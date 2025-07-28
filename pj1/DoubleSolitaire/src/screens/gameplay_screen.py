import pygame

from src.config import config_manager
from src.ai.template import TemplateAi
from src.submenu.game_sidebar import Sidebar
from src.submenu.options_menu import OptionsMenu
from src.ai.heuristics import Heuristics
from src.ai.algorithms import UniformCostSearch
from src.ai.algorithms import DFS


from src.gameplay.gameplay_events import (
    human_handle_mouse_button_up,
    human_handle_mouse_button_down,
    human_handle_mouse_motion,
    handle_keydown
)

from src.gameplay.gameplay_logic import (
    deal_cards,
    check_win,
    check_auto_moves,
    ai_update,
    get_score
)

from src.utils.game_loader import GameLoader
from src.elements.card_slot import CardSlot
from src.elements.cards import Cards
from src.utils.assets import AssetManager
from src.utils.mouse import get_virtual_mouse_pos
from src.animations.object_move import ObjectMove


class GameplayScreen:
    """
        Handles the gameplay screen including rendering the background, slots, foundations,
        and managing card interactions such as dragging and dropping.
    """
    def __init__(self):
        """
        Initialize the gameplay screen by setting up virtual dimensions, loading assets,
        creating and shuffling the deck, initializing card movement variables, and
        creating card slots and foundations. Finally, deals the cards evenly into the slots.
        """
        self.ai_player = config_manager.gamePlayerType
        self.base_width = 480
        self.base_height = 270

        self.double_click_delay = 400
        self.anim_duration = self._get_anim_speed(config_manager.gameFastMode,config_manager.gameNoAnims)
        self.last_click_time = 0

        self.active_animations = []

        self._load_assets()
        self.is_started = False

        self.nochange = 0

        self.time_limit = config_manager.gameTimeLimit * 60
        self.time_elapsed = 0
        self.moves_used = 0
        self.last_time_tick = pygame.time.get_ticks()
        self.move_limit = 100
        self.score = 0

        self.sidebar = Sidebar(
            x=480-71,
            y=0,
            width=71,
            height=270,
            font=self.font
        )

        self.cards = Cards("assets/images/1.2Pokercards.png")
        self.cards.shuffle()

        self._init_card_movement_variables()

        self.slots = self._create_slots()
        self.foundations = self._create_foundations()

        self.options = OptionsMenu()
        self.isOptions = False

        self.is_won = False

        self.is_lose = False

        self.move_stack = []

        if not config_manager.gameLoadGame :
            deal_cards(self)
        else:
            json_path = GameLoader.ask_for_game_file()
            json_data = GameLoader.load_json(json_path)
            if json_data :
                self.slots, self.foundations = GameLoader.populate_slots(self.cards,json_data, self.slots, self.foundations)
            else:
                self.slots = None

        self.move_stack.append(GameLoader.generate_json(self.slots, self.foundations))
        self.ai = self._create_ai()

      



    def _load_assets(self):
        """
        Loads background images and fonts used
        """
        self.bg = AssetManager.load_image("assets/images/backgrounds/BackgroundWoodTilesDimmed.png")
        self.font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf", 13)
        self.bg_foundation = AssetManager.load_image("assets/images/Foundation.png")
        self.bg_holder = AssetManager.load_image("assets/images/Holder.png")



    def _init_card_movement_variables(self):
        """
        Initialize variables used for handling card dragging.
        """
        self.selected_card = None
        self.selected_stack = []
        self.drag_offset = (0, 0)
        self.original_slot = None

    def _create_slots(self):
        """
        Create the playing slots where cards will be dealt.
        """
        slots = []
        slot_spacing = 51
        num_slots = 13
        x_start = 4
        y_start = 14

        for i in range(num_slots):
            col_pos = i // 7  # Determine the column position for rows
            x = x_start + (i % 7) * slot_spacing
            y = y_start + col_pos * 119
            slot = CardSlot(position=(x, y), vertical_offset=14, bg_sprite=self.bg_holder, mv_rules=config_manager.gameStackMovement,sk_size=config_manager.gameStackSize)
            slots.append(slot)
        return slots

    def _create_foundations(self):
        """
        Create the foundation slots where cards are built in sequence.
        """
        foundations = []
        foundation_x = 360
        foundation_offset = 67
        foundation_start_y = 2

        for i in range(4):
            x = foundation_x
            y = foundation_start_y + i * foundation_offset
            foundation = CardSlot(position=(x, y), vertical_offset=0, is_foundation=True, bg_sprite=self.bg_foundation)
            foundations.append(foundation)
        return foundations

    def _get_anim_speed(self,isFastMode, isNoAnims):
        if isFastMode:
            return 150
        elif isNoAnims:
            return 1
        return 2000

    def _create_ai(self):
        match self.ai_player:
            case 1:
                ai = TemplateAi()
            case 2:
                ai = DFS(self)
            case 3:
                ai = UniformCostSearch(self)
            case _:
                self.ai_player = 0
                ai = None
        return ai

    def _reload_config(self):
        self.anim_duration = self._get_anim_speed(config_manager.gameFastMode,config_manager.gameNoAnims)

    def handle_event(self, event):
        """

        :param event: The event to handle.
        :return: A command string("back_to_menu","quit_game") or None
        """

        if self.isOptions:
            should_close, state_number = self.options.handle_event(event)
            if should_close:
                self.isOptions = False
                self._reload_config()
                if state_number != -1:
                    print(state_number)
                    self.load_from_move_stack(state_number)

        mouse_pos = get_virtual_mouse_pos(480,270)


        # handle sidebar
        if self.sidebar.rect.collidepoint(mouse_pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                ret = self.sidebar.handle_event(event)
                if ret == "back_to_menu":
                    return "back_to_menu"
                elif ret == "options":
                    self.isOptions = True
                    self.options.set_num_states(len(self.move_stack))
                    self.options.state_number = -1
                elif ret == "save":
                    json_path = GameLoader.ask_for_save_file()
                    if json_path is None:
                        self.sidebar.buttons[-1].change_color((255,0,0))
                        return
                    json_data = GameLoader.generate_json(self.slots, self.foundations)
                    GameLoader.save_json(json_path, json_data)
                    self.sidebar.buttons[-1].change_color((0,200,0))
                elif ret == "hint":
                    self.show_hint()
                elif ret == "undo":
                    if len(self.move_stack) > 2:
                        self.load_from_move_stack(-2)
                        print(len(self.move_stack))
                        for slot in self.slots + self.foundations:
                            slot.reposition_cards()
                    return
                else:
                    return None

        if self.is_won or self.is_lose:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart_game"  # Reiniciar o jogo
                elif event.key == pygame.K_m:
                    return "back_to_menu"  # Voltar ao menu principal
            return None

        if self.ai_player == 0:
            if event.type == pygame.KEYDOWN:
                return handle_keydown(self,event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                human_handle_mouse_button_down(self,event)
            elif event.type == pygame.MOUSEMOTION:
                human_handle_mouse_motion(self,event)
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                human_handle_mouse_button_up(self,event)

        if self.ai_player != 0:
            #Handle inputs like: pause, skip anim
            return None
        olddata = ""
        if len(self.move_stack) > 0:
            olddata = self.move_stack[-1]

        newdata = GameLoader.generate_json(self.slots, self.foundations)
        if olddata != newdata:
            self.move_stack.append(newdata)
            self.sidebar.set_score(get_score(self))



        return None

    def load_from_move_stack(self, i):
        data = self.move_stack[i]
        self.move_stack = self.move_stack[:i]
        self.cards.restore()
        ns,nf = self._create_slots(),self._create_foundations()
        ns, nf = GameLoader.populate_slots(self.cards,data, ns, nf)
        if ns is not None and nf is not None:
            self.slots, self.foundations = ns,nf
            self.options.set_num_states(len(self.move_stack))
        self.sidebar.set_score(get_score(self))


    def _handle_double_click(self, mouse_pos):
        """
        Handle double click events.
        :param mouse_pos: Mouse position
        """
        for slot in self.slots:
            if slot.cards:
                for card in reversed(slot.cards):
                    if card.rect.collidepoint(mouse_pos):
                        self.auto_move_to_foundation(card, slot)
                        return

    def auto_move_to_foundation(self, card, from_slot):
        """
        Automatically move a card to the correct foundation slot if it's allowed.

        :param card: The card to move
        :param from_slot: The slot from which the card is being moved.
        """
        for foundation in self.foundations:
            if foundation.drop_card(card, from_slot, to_animate=True):
                target_pos = foundation.position
                animation = ObjectMove(
                    anim_obj=card,
                    start_pos=card.rect.topleft,
                    target_pos=target_pos,
                    duration=self.anim_duration,
                    on_complete=lambda : foundation.reposition_cards()
                )
                self.active_animations.append(animation)

                self.hint_card = None
                self.hint_slot = None

                return
            from_slot.reposition_cards()

    def update(self):
        """
        Updates Slots and Foundations
        Might be used for animations
        
        Handles AI (Updates 60 times p/s so each move must either be animated or have a cd)
        """
        if self.isOptions:
            self.options.update()
            return
        if self.is_won: # TODO ADICIONAR O LOSE
            return

        now = pygame.time.get_ticks()
        if now - self.last_click_time >= 1000:
            self.time_elapsed += 1
            self.last_click_time = now

            time_left = max(self.time_limit - self.time_elapsed, 0)
            minutes = time_left // 60
            second = time_left % 60
            self.sidebar.set_time_left(f"{minutes:02}:{second:02}")
            #self.sidebar.set_score(self.score)

            if len(self.active_animations) == 0:
                if time_left <= 0:
                    self.is_lose = True



        '''if len(self.active_animations) == 0:
            if (Heuristics.available_moves(self) == 0):
                self.is_lose = True

            if (Heuristics.available_moves(self) == 1):
                if(self.nochange == 6):
                    self.is_lose = True
                self.nochange += 1

            if(Heuristics.available_moves(self) != 1):
                self.nochange = 0'''

        
        if not self.is_started:
            if self.slots is None:
                return "back_to_menu"
            to_update = check_auto_moves(self.slots, self.foundations)
            for i,v in to_update:
                self.auto_move_to_foundation(i,v)
            self.sidebar.set_score(get_score(self))
            self.is_started = True

        for slot in self.slots + self.foundations:
            slot.update()

        mid_anim = False
        for animation in self.active_animations:
            animation.update()
            if not animation.active:
                self.active_animations.remove(animation)
            mid_anim = True

        if mid_anim:
            return

        to_update = check_auto_moves(self.slots, self.foundations)
        for i,v in to_update:
            self.auto_move_to_foundation(i,v)

        if to_update:
            self.sidebar.set_score(get_score(self))
            return
        ai_update(self)
        check_win(self)

    def render(self, screen):
        """
        Renders the screen, background, slots and foundations as well as the currently dragged stack/card
        :param screen: The screen to render.
        """
        if self.slots is None:
            return
        screen.blit(self.bg, (0, 0))
        self.sidebar.draw(screen)
        for slot in self.slots:
            slot.draw_background(screen)
        for foundation in self.foundations:
            foundation.draw_background(screen)

        for slot in self.slots:
            slot.draw_cards(screen)
        for foundation in self.foundations:
            foundation.draw_cards(screen)

        if self.selected_stack:
            for card in self.selected_stack:
                screen.blit(card.image, card.rect.topleft)

        for animation in self.active_animations:
            # Ensure the animated card is drawn last, using its updated rect
            screen.blit(animation.anim_obj.image, animation.anim_obj.rect.topleft)
        
        if hasattr(self, 'hint_card') and self.hint_card:
            highlight_color = (255, 215, 0)  # Dourado brilhante
            border_thickness = 4
            pygame.draw.rect(
                screen,
                highlight_color,
                self.hint_card.rect.inflate(10, 10),  # Aumenta o tamanho do retângulo para criar bordas
                border_thickness,
                border_radius=8  # Bordas arredondadas
        )
        if hasattr(self, 'hint_slot') and self.hint_slot:
            highlight_color = (0, 255, 0)  # Verde brilhante para o destino
            border_thickness = 4
            if isinstance(self.hint_slot, CardSlot) and self.hint_slot.cards:
                top_card = self.hint_slot.top_card()
                pygame.draw.rect(
                    screen,
                    highlight_color,
                    top_card.rect.inflate(10, 10), 
                    border_thickness,
                    border_radius=8  
            )


        if self.isOptions:
            self.options.draw(screen)

        if self.is_won:
            self._render_win_screen(screen)
            return
        
        if self.is_lose:
            self._render_lose_screen(screen)
            return

    def _render_win_screen(self, screen):
    
        # Renderizar o fundo animado (reutilizando o fundo do jogo)
        screen.blit(self.bg, (0, 0))

        # Renderizar o texto de vitória
        title_font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf", 52)
        victory_text = title_font.render("Congratulations!", False, (255, 215, 0))  # Texto dourado
        victory_rect = victory_text.get_rect(center=(self.base_width // 2, self.base_height // 2 - 100))
        screen.blit(victory_text, victory_rect)

        # Renderizar subtítulo
        subtitle_font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf", 36)
        subtitle_text = subtitle_font.render("You Win!", False, (255, 255, 255))  # Texto branco
        subtitle_rect = subtitle_text.get_rect(center=(self.base_width // 2, self.base_height // 2 - 60))
        screen.blit(subtitle_text, subtitle_rect)

        icon = AssetManager.load_image("assets/images/icons/IconLarge.png")
        new_width = icon.get_width() * 0.75
        new_height = icon.get_height() * 0.75
        icon = pygame.transform.scale(icon, (new_width, new_height))  
        icon_rect = icon.get_rect(center=(self.base_width // 2, self.base_height // 2 + 10))  
        screen.blit(icon, icon_rect)

        score_font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf", 26)
        score_text = score_font.render(f"Score: {self.score}", False, (255, 255, 255)) 
        score_rect = score_text.get_rect(center=(self.base_width // 2, self.base_height // 2 + 80))
   
        
        # Renderizar opções para o jogador
        option_font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf", 26)
        restart_text = option_font.render("Press R to Restart", False, (255, 255, 255))  # Texto branco
        menu_text = option_font.render("Press M to Return to Menu", False, (255, 255, 255))

        restart_rect = restart_text.get_rect(center=(self.base_width // 2, self.base_height // 2 + 100))
        menu_rect = menu_text.get_rect(center=(self.base_width // 2, self.base_height // 2 + 120))

        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(menu_text, menu_rect)

        

    def get_hint(self):
        """
        Analisa o estado atual do jogo e retorna a carta e o slot de destino para a dica.
        Prioriza movimentos entre slots para cores diferentes, depois para o mesmo naipe,
        e por último verifica se a carta pode ir para a fundação.
        :return: (card, slot) ou None se não houver movimentos válidos.
        """
        # 1. Priorizar movimentos entre slots para cores diferentes
        for source_slot in self.slots:
            card = source_slot.top_card()
            if card:
                for target_slot in self.slots:
                    if target_slot != source_slot and target_slot.can_accept_card(card):
                        # Verificar se as cores são diferentes
                        if card.suit in ['Hearts', 'Diamonds'] and target_slot.top_card().suit in ['Spades', 'Clubs']:
                            return card, target_slot
                        if card.suit in ['Spades', 'Clubs'] and target_slot.top_card().suit in ['Hearts', 'Diamonds']:
                            return card, target_slot

        # 2. Movimentos entre slots para o mesmo naipe
        for source_slot in self.slots:
            card = source_slot.top_card()
            if card:
                for target_slot in self.slots:
                    if target_slot != source_slot and target_slot.can_accept_card(card):
                        # Verificar se os naipes são iguais
                        if card.suit == target_slot.top_card().suit:
                            return card, target_slot

        # 3. Movimentos para as fundações
        for slot in self.slots:
            card = slot.top_card()
            if card:
                for foundation in self.foundations:
                    if foundation.can_accept_card(card):
                        return card, foundation

        # Nenhum movimento válido encontrado
        return None

    def show_hint(self):
        """
        Mostra uma dica ao jogador destacando a carta e o slot de destino.
        """
        hint = self.get_hint()
        if hint:
            card, destination = hint  # O destino pode ser um slot ou uma fundação
            print(f"Dica: Mova a carta {card} para {type(destination).__name__}.")  # Mensagem no console
            # Destacar a carta e o slot de destino
            self.hint_card = card
            self.hint_slot = destination
        else:
            print("Nenhuma dica disponível no momento.")  # Mensagem no console
            self.hint_card = None
            self.hint_slot = None

    def _render_lose_screen(self, screen):
        
            # Renderizar o fundo animado (reutilizando o fundo do jogo)
            screen.blit(self.bg, (0, 0))

            # Renderizar o texto de derrota
            title_font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf", 52)
            victory_text = title_font.render("Better luck next time...", False, (255, 215, 0))  # Texto dourado
            victory_rect = victory_text.get_rect(center=(self.base_width // 2, self.base_height // 2 - 100))
            screen.blit(victory_text, victory_rect)

            # Renderizar subtítulo
            subtitle_font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf", 36)
            subtitle_text = subtitle_font.render("You Lose", False, (255, 255, 255))  # Texto branco
            subtitle_rect = subtitle_text.get_rect(center=(self.base_width // 2, self.base_height // 2 - 60))
            screen.blit(subtitle_text, subtitle_rect)


            icon = AssetManager.load_image("assets/images/icons/IconLarge.png")
            new_width = icon.get_width() * 0.75
            new_height = icon.get_height() * 0.75
            icon = pygame.transform.scale(icon, (new_width, new_height))  
            icon_rect = icon.get_rect(center=(self.base_width // 2, self.base_height // 2 + 10))  
            screen.blit(icon, icon_rect)
            

            # Renderizar opções para o jogador
            option_font = AssetManager.load_font("assets/fonts/C&C Red Alert [INET].ttf", 26)
            restart_text = option_font.render("Press R to Restart", False, (255, 255, 255))  # Texto branco
            menu_text = option_font.render("Press M to Return to Menu", False, (255, 255, 255))

            restart_rect = restart_text.get_rect(center=(self.base_width // 2, self.base_height // 2 + 80))
            menu_rect = menu_text.get_rect(center=(self.base_width // 2, self.base_height // 2 + 100))

            screen.blit(restart_text, restart_rect)
            screen.blit(menu_text, menu_rect)

    




