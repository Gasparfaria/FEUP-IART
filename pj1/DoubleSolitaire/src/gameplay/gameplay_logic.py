from src.animations.object_move import ObjectMove
from src.utils.card_order import min_rank, is_next_rank



def deal_cards(self):
    """
    Deal the shuffled deck of cards evenly into the available slots.
    """
    num_slots = len(self.slots)
    for i, card in enumerate(self.cards.cards):
        slot_index = i % num_slots
        self.slots[slot_index].add_card(card)
    for slot in self.slots:
        slot.push_king_to_top()

def check_win(self):
    total_cards_in_foundations = sum(len(foundation.cards) for foundation in self.foundations)
    if total_cards_in_foundations == 52:
        self.is_won = True
        last_score = 15 * max(self.time_limit - self.time_elapsed, 0)
        self.score += last_score

def check_auto_moves(slots, foundations):
    min_foundation = None
    for foundation in foundations:
        if foundation.top_card() is None:
            min_foundation = None
            break
        min_foundation = min_rank(foundation.top_card().rank, min_foundation)
    to_update = []

    for slot in slots:
        card = slot.top_card()
        if card is None:
            continue
        if is_next_rank(min_foundation, card.rank):
            to_update.append((slot.top_card(), slot))
    return to_update

def ai_update(self):
    """
    Updates the game state by calling the AI class to calculate the next move and performing animations
    for the determined move. This method is executed during each update cycle when AI is active.

    The AI analyzes the current game state, determines the best action to perform (e.g., moving a card
    to a foundation or another slot), and applies the action. If animations are required for the move,
    they are created and managed within this method.

    This ensures smooth and logical gameplay progression under AI control.
    """
    if self.ai is None:
        return

    orig_slot, card, target_slot = self.ai.get_move()

    if orig_slot == 0 and card == 0 and target_slot == 0:
        return

    if orig_slot > 12:
        orig_slot = self.foundations[orig_slot-13]
    else:
        orig_slot = self.slots[orig_slot]
    if target_slot > 12:
        target_slot = self.foundations[target_slot-13]
    else:
        target_slot = self.slots[target_slot]

    print(orig_slot.top_card())
    print(card)
    print(target_slot.top_card())

    if target_slot.can_accept_card(card):
        stack = target_slot.check_if_can_drop(card, orig_slot)
        if not target_slot.drop_card(card, orig_slot, to_animate=True):
            print("AI move failed")
            return
        if stack:
            for i,card in enumerate(stack):
                target_pos_x,target_pos_y = target_slot.position
                target_pos_y += target_slot.vertical_offset * (i + len(target_slot.cards)-1)
                animation = ObjectMove(
                    anim_obj=card,
                    start_pos=card.rect.topleft,
                    target_pos=(target_pos_x, target_pos_y),
                    duration=self.anim_duration,
                    on_complete=lambda: target_slot.reposition_cards()
                )
                self.active_animations.append(animation)
        else:
            target_pos_x, target_pos_y = target_slot.position
            target_pos_y += target_slot.vertical_offset * (len(target_slot.cards) -1)
            animation = ObjectMove(
                anim_obj=card,
                start_pos=card.rect.topleft,
                target_pos=(target_pos_x, target_pos_y),
                duration=self.anim_duration,
                on_complete=lambda: target_slot.reposition_cards()
            )
            self.active_animations.append(animation)

def get_score(self):
    score = 0
    for foundation in self.foundations:
        score += len(foundation.cards) * 50

    return score
