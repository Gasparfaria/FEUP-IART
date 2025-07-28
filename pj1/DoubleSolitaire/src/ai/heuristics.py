from src.elements.card_slot import CardSlot
from src.utils.card_order import rank_index
from src.utils.card_order import is_prev_rank
  
class Heuristics:
    def __init__(self, game):
        self.game = game
    
    def cards_in_foundation(gameplay_screen):
        cards_in_foundation = 0
        for foundation in gameplay_screen.foundations:
            cards_in_foundation += len(foundation.cards)
        return cards_in_foundation

    def available_moves(gameplay_screen):
        available_moves = 0
        for source_slot in gameplay_screen.slots:
            card = source_slot.top_card()
            if card:
                for target_slot in gameplay_screen.slots:
                    if target_slot.can_accept_card(card):
                        available_moves += 1

        for slot in gameplay_screen.slots:
            card = slot.top_card()
            if card:
                for foundation in gameplay_screen.foundations:
                    if foundation.can_accept_card(card):
                        available_moves += 1
        return available_moves
    
    def distance_to_foundation(gameplay_screen):
   
        closest_distance = 13  

        rank_map = {"Ace": 1, "King": 13, "Queen": 12, "Jack": 11}  

        for source_slot in gameplay_screen.slots:
            card = source_slot.top_card()
          
            if card is None:
                continue  

            #print(f"Card: {card.rank} of {card.suit}")

            try:
                card_level = int(card.rank)
            except ValueError:
                card_level = rank_map.get(card.rank, None)  

    

            for foundation in gameplay_screen.foundations:
                last_card_in_foundation = foundation.top_card()

                if last_card_in_foundation is None:
                    continue  

                #print(f"Foundation Card: {last_card_in_foundation.rank} of {last_card_in_foundation.suit}")

                try:
                    level_foundation = int(last_card_in_foundation.rank)
                except ValueError:
                    level_foundation = rank_map.get(last_card_in_foundation.rank, None)

                if level_foundation is None or card_level is None:
                    continue  

                distance = card_level - level_foundation

                #print(f"Distance: {distance}")

                if distance >= 0 and closest_distance > distance:  # Ensure distance is valid
                    closest_distance = distance

        return 13 - closest_distance

    
    def blocked_cards(gameplay_screen):
        blocked_count = 0
        for slot in gameplay_screen.slots:
            for i in range(len(slot.cards) - 1):
                current_card = slot.cards[i]
                next_card = slot.cards[i + 1]
                
                current_rank_index = rank_index(current_card.rank)
                next_rank_index = rank_index(next_card.rank)
                
                if not (current_rank_index == next_rank_index + 1 and current_card.suit != next_card.suit):
                    blocked_count += 1
        return blocked_count

    @staticmethod
    def sequential_progress(gameplay_screen):
        descending_columns = 0

        for slot in gameplay_screen.slots:
            if len(slot.cards) < 2:
                continue 

            is_descending = True
            for i in range(len(slot.cards) - 1):
                current_card = slot.cards[i]
                next_card = slot.cards[i + 1]

                
                if not is_prev_rank(current_card.rank, next_card.rank):
                    is_descending = False
                    break

            if is_descending:
                descending_columns += 1

        return descending_columns

    def weighted_combination(gameplay_screen):
        
            cards_foundation = Heuristics.cards_in_foundation(gameplay_screen) * 1.5
            available_moves = Heuristics.available_moves(gameplay_screen) * 1.0
            distance = Heuristics.distance_to_foundation(gameplay_screen) * 1.0
            blocked_cards = Heuristics.blocked_cards(gameplay_screen) * 1.0
            sequential_progress = Heuristics.sequential_progress(gameplay_screen) * 1.5


            return cards_foundation + available_moves + distance + blocked_cards + sequential_progress
