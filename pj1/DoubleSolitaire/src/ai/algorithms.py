import time
import tracemalloc
from src.utils.game_loader import GameLoader
from src.gameplay.gameplay_logic import check_auto_moves
from src.config import config_manager

class DFS:
    def __init__(self, gameplay_screen, max_depth=1000):
        self.gameplay_screen = gameplay_screen
        self.visited_states = set()  # Para evitar ciclos
        self.solution_path = []  # Para armazenar o caminho até o estado de vitória
        self.new_solution_path = []
        self.max_depth = max_depth

        # Iniciar medição de tempo e memória
        tracemalloc.start()
        start_time = time.time()

        # Executar o algoritmo
        found = self.dfs()
        if not found:
            self.solution_path = []


        # Parar medição de tempo e memória
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Calcular métricas
        execution_time = end_time - start_time
        memory_usage = peak / 1024  # Converter para KB

        # Guardar métricas num ficheiro
        self.save_metrics("DFS", execution_time, memory_usage)

        self.index = 0
        print(self.solution_path)

        translate_solution_to_index(self)
        if not self.solution_path:
            gameplay_screen.is_lose = True

        print(self.new_solution_path)
        self.gameplay_screen.load_from_move_stack(0)

    def dfs(self, depth=0):
        """
        Implementa o algoritmo DFS para encontrar o estado de vitória.
        """
        if depth > self.max_depth:
            return False  # Limite de profundidade atingido

        # Verifica se o estado atual é um estado de vitória
        if is_win_state(self):
            return True

        # Gera os movimentos possíveis
        possible_moves = get_possible_moves(self)

        for move in possible_moves:
            # Aplica o movimento
            apply_move(self, move)

            # Gera a chave do estado atual
            state_key = get_state_key(self)

            # Verifica se o estado já foi visitado
            if state_key not in self.visited_states:
                self.visited_states.add(state_key)
                self.solution_path.append(move)

                # Chama recursivamente o DFS
                if self.dfs(depth + 1):
                    return True

                # Remove o movimento do caminho da solução
                self.solution_path.pop()

            # Desfaz o movimento
            undo_move(self, move)

        return False

    def save_metrics(self, algorithm_name, execution_time, memory_usage):
        """
        Guarda as métricas de execução num ficheiro de texto.
        """
        with open("metrics.txt", "a") as file:
            file.write(f"Algorithm: {algorithm_name}\n")
            file.write(f"Execution Time: {execution_time:.4f} seconds\n")
            file.write(f"Memory Usage: {memory_usage:.2f} KB\n")
            file.write(f"Solution Path: {self.solution_path}\n")
            file.write("-" * 40 + "\n")

    def get_move(self):
        if self.index < len(self.new_solution_path):
            move = self.new_solution_path[self.index]

            self.index += 1

            return move
        else:
            #print("can't do more moves")
            return 0,0,0

class BFS:
    def bfs(self):
        """
        Implementa o algoritmo BFS para encontrar o estado de vitória.
        """
        queue = deque()
        initial_state_key = get_state_key(self)
        queue.append((initial_state_key, []))  # Estado inicial e caminho vazio
        self.visited_states.add(initial_state_key)

        while queue:
            current_state_key, path_so_far = queue.popleft()

            # Aplica os movimentos do caminho até o estado atual
            for move in path_so_far:
                apply_move(self, move)

            # Verifica se o estado atual é um estado de vitória
            if is_win_state(self):
                self.solution_path = path_so_far
                return True

            # Gera os movimentos possíveis
            possible_moves = get_possible_moves(self)

            for move in possible_moves:
                apply_move(self, move)
                new_state_key = get_state_key(self)

                # Adiciona o novo estado à fila se ainda não foi visitado
                if new_state_key not in self.visited_states:
                    self.visited_states.add(new_state_key)
                    queue.append((new_state_key, path_so_far + [move]))

                # Desfaz o movimento para voltar ao estado anterior
                undo_move(self, move)

            # Desfaz os movimentos aplicados para retornar ao estado inicial deste nó
            for move in reversed(path_so_far):
                undo_move(self, move)

        return False

    def get_move(self):
        if self.index < len(self.new_solution_path):
            move = self.new_solution_path[self.index]
            self.index += 1
            return move
        else:
            return 0, 0, 0

import heapq
from src.ai.heuristics import Heuristics

class UniformCostSearch:
    def __init__(self, gameplay_screen):
        self.gameplay_screen = gameplay_screen

        self.visited_states = {}  
        self.solution_path = []

        self.new_solution_path = []

        found = self.search()
        self.index = 0
        print(self.solution_path)

        translate_solution_to_index(self)
        print(self.new_solution_path)

        print(found)
        self.gameplay_screen.load_from_move_stack(0)

    
    def get_move(self):
        if self.index < len(self.new_solution_path):
            move = self.new_solution_path[self.index]

            self.index += 1

            return move
        else:
            #print("can't do more moves")
            return 0,0,0



    def move_cost(self, gameplay_screen):
        score = Heuristics.weighted_combination(gameplay_screen)
        return 1000 - score  # Don't know if 1000 is too much or too little, I'll tweak it later

    def search(self):
        queue = []
        initial_state_key = get_state_key(self)
        heapq.heappush(queue, (0,0, [], initial_state_key))

        self.visited_states[initial_state_key] = 0

        while queue:
            total_cost, _, path_so_far, state_key = heapq.heappop(queue)


            for move in path_so_far:
                apply_move(self,move)

            if is_win_state(self):
                self.solution_path = path_so_far
                for move in reversed(path_so_far):
                    undo_move(self,move)
                return True


            for move in get_possible_moves(self):
                apply_move(self,move)
                new_state_key = get_state_key(self)

                move_c = self.move_cost(self.gameplay_screen)
                new_cost = total_cost + move_c

                if new_state_key not in self.visited_states or new_cost < self.visited_states[new_state_key]:
                    self.visited_states[new_state_key] = new_cost
                    heapq.heappush(queue, (new_cost, len(path_so_far) + 1, path_so_far + [move], new_state_key))

                undo_move(self,move)

        return False

def apply_move(self, move):
    source_slot, card, target_slot = move
    target_slot.drop_card(card, source_slot)
    auto_moves = check_auto_moves(self.gameplay_screen.slots, self.gameplay_screen.foundations)
    if auto_moves:
        for i, v in auto_moves:
            for foundation in self.gameplay_screen.foundations:
                foundation.drop_card(i, v, to_animate=False)


def undo_move(self, move):
    source_slot, card, target_slot = move
    source_slot.undo_drop_card(card, target_slot)


def get_state_key(self):
    state_key = []
    for slot in self.gameplay_screen.slots:
        state_key.append(tuple(card.rank for card in slot.cards))
    for foundation in self.gameplay_screen.foundations:
        state_key.append(tuple(card.rank for card in foundation.cards))
    return tuple(state_key)

def get_possible_moves(self):
    moves = []
    if config_manager.gameStackSize == 1:
        for source_slot in self.gameplay_screen.slots:
            card = source_slot.top_card()
            if card:
                for target_slot in self.gameplay_screen.slots:
                    if target_slot != source_slot and target_slot.can_accept_card(card):
                        moves.append((source_slot, card, target_slot))
                for foundation in self.gameplay_screen.foundations:
                    if foundation.can_accept_card(card):
                        moves.append((source_slot, card, foundation))
    else:
        for source_slot in self.gameplay_screen.slots:
            for card in source_slot.cards:
                if card:
                    for target_slot in self.gameplay_screen.slots:
                        if target_slot != source_slot and target_slot.can_accept_card(card):
                            moves.append((source_slot, card, target_slot))
                    for foundation in self.gameplay_screen.foundations:
                        if foundation.can_accept_card(card):
                            moves.append((source_slot, card, foundation))
    return moves

def is_win_state(self):
    """
    Verifica se o estado atual é um estado de vitória.
    """
    total_cards_in_foundations = sum(len(foundation.cards) for foundation in self.gameplay_screen.foundations)
    return total_cards_in_foundations == 52




def translate_solution_to_index(self):
    slots = self.gameplay_screen.slots
    foundations = self.gameplay_screen.foundations
    for i, card, k in self.solution_path:
        if i in slots:
            ni = slots.index(i)
        elif i in foundations:
            ni = 13 + foundations.index(i)
        else:
            raise ValueError(f'Value {i} not found in slots or foundations.')

        if k in foundations:
            nk = len(slots) + foundations.index(k)
        elif k in slots:
            nk = slots.index(k)
        else:
            raise ValueError(f'Value {k} not found in foundations or slots.')

        new_move = (ni, card, nk)
        self.new_solution_path.append(new_move)
