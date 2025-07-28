import json
import tkinter as tk
from tkinter import filedialog, messagebox


class GameLoader:
    """
    Helper Class to load game data from a file

    Also handles writing to file
    """
    @classmethod
    def ask_for_game_file(cls):
        """
        Asks the user to select a game file

        :return: Selected file_path
        """

        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Select a saved game file",
            filetypes=[("Save Files", "*.save"), ("All Files", "*.*")]
        )
        if file_path:
            return file_path
        else:
            return None

    @classmethod
    def ask_for_save_file(cls):
        """
        Asks the user to select a place to save a game file

        :return: File path selected
        """
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.asksaveasfilename(
            title="Select location to save the game",
            defaultextension=".save",
            filetypes=[("Save Files", "*.save"), ("All Files", "*.*")]
        )
        print(file_path)
        return file_path if file_path else None

    @classmethod
    def populate_slots(cls, deck, json_data, slots, foundations):
        """
        Function to load json data

        Checks if the json_data is valid. If nº cards != 52 invalid, if len(slots) > 4 invalid
        Every time, the corresponding card is taken from the deck ensuring no duplicated cards

        If its invalid returns None,None

        :param deck: The created deck
        :param json_data: Json_data containing game_state
        :param slots: List of CardSlot objects -> is_foundation = false
        :param foundations: List of CardSlot objects -> is_foundation = true
        :return: Filled slots,foundations
        """
        try:
            card_count = 0
            for i,slot in enumerate(json_data["slots"].values()):
                for card in slot:
                    deck_card = deck.pop(card["suit"],card["rank"])
                    if deck_card is not None:
                        slots[i].add_card(deck_card)
                        card_count += 1
                    else:
                        cls.show_error(f"Missing card: {card} not found in deck.")


            for i,slot in enumerate(json_data["foundations"].values()):
                for card in slot:
                    deck_card = deck.pop(card["suit"], card["rank"])
                    if deck_card is not None:
                        foundations[i].add_card(deck_card)
                        card_count += 1
                    else:
                        cls.show_error(f"Missing card: {card} not found in deck.")
            if card_count == 52:
                return slots, foundations
            return None,None
        except Exception as e:
            cls.show_error(f"Error loading Json, not available: {e}")
            return None, None

    @classmethod
    def generate_json(cls,slots, foundations):
        slots_dict = {}
        for i,slot in enumerate(slots):
            name = f's{i+1}'
            cards = [{"suit": card.suit, "rank": card.rank} for card in slot.cards]
            slots_dict[name] = cards

        foundations_dict = {}
        for i,foundations in enumerate(foundations):
            name = f'f{i+1}'
            cards = [{"suit": card.suit, "rank": card.rank} for card in foundations.cards]
            foundations_dict[name] = cards


        data = {
            "slots" : slots_dict,
            "foundations" : foundations_dict
        }

        return data


    @classmethod
    def load_json(cls,file_path):
        """
        Loads a json save
        :param file_path: File path
        :return: json_data
        """
        try:
            with open(file_path) as json_file:
                json_data = json.load(json_file)
                return json_data
        except Exception as e:
            cls.show_error("Error loading game json file: \n" + str(e))

    @classmethod
    def save_json(cls,file_path,json_data):
        """
        Saves a game state into a json file

        :param file_path: Path to save into
        :param json_data: Data to be saved
        """

        if file_path is None:
            cls.show_error("File path cannot be None")
        try:
            with open(file_path, 'w') as json_file:
                json.dump(json_data, json_file)
        except Exception as e:
            cls.show_error("Error saving game json file: \n" + str(e))

    @classmethod
    def show_error(cls, message):
        """
        Helper function to show a message in case of an error

        :param message: Message to show
        """
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Game Loader Error", message)