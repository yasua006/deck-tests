import random
from dataclasses import dataclass
import sys
import os
from time import sleep
import emoji

from personal_logging.main import error, warn
import questionary


@dataclass
class Cards:
    """
    Cards are shuffled on init
    Shuffle cards again with existing class method
    Debug cards with existing class method or using the instance vars
    """

    def __post_init__(self) -> None:
        # Source - https://stackoverflow.com/a/48677535
        # Posted by Turn, modified by community. See post 'Timeline' for change history
        # Retrieved 2026-06-08, License - CC BY-SA 3.0
        self.deck = [(suit, v) for suit in ['❤️', '♠️', '♣️', '♦️'] 
                for v in [str(i) for i in range(2, 11)] + list("JKQA")]
        self.deck_list = [" ".join(thing) for thing in self.deck]

        self.shuffle_cards()
        #print("Shuffled cards on init!")


    def inv_deck_count(self) -> bool:
        if len(self.deck_list) <= 0:
            error("Invalid or low card count for deck!")
            return True

        return False


    def shuffle_cards(self) -> None:
        random.shuffle(self.deck_list)

    def draw_card(self) -> str:
        """
        Draws a card from backwards (face down deck)

        -----
        Returns a string, if you cannot draw a card
        """

        if self.inv_deck_count(): return "Cannot draw a card!"

        return self.deck_list.pop()

    def debug_cards(self) -> None:
        """
        Warns the total amount of cards
        Logs the deck itself, visible like magic
        """

        card_amount: int = len(self.deck_list)
        warn(f"Total cards: {card_amount}")
        print(", ".join((self.deck_list)))


@dataclass
class Table:
    """
    Table cards exist on init
    Debug table cards with existing class method or using the instance vars

    -----
    This does not handle stacked cards (cards on top of each other!)
    """

    name: str = ""

    rnd_card_amount: int = 4
    """ The card amount to put on the table using the deck """

    def __post_init__(self) -> None:
        self.table_cards: list[str] = []

    def show_table_cards(self) -> None:
        print(f"\nTable cards: {', '.join(self.table_cards)}\n")


@dataclass
class Player:
    """
    New hand on init
    Captures are disabled by default
    Debug the player with existing class method or using the instance vars

    -----
    Errors, if both capture booleans are set to True
    """

    name: str
    deck: Cards
    new_hand_amount: int = 3

    is_table_captures: bool = False
    """ Captures are left on the table face down """
    is_hand_captures: bool = False
    """ Captures increment player card(s)"""

    def __post_init__(self) -> None:
        if self.is_table_captures and self.is_hand_captures:
            error("Player cannot capture both ways: table and hand!")
            return

        self.plr_cards: list[str] = []

        if self.is_table_captures:
            self.table_captures = []

        self.new_hand()

    def new_hand(self) -> None:
        for _ in range(self.new_hand_amount):
            self.plr_cards.append(self.deck.draw_card())

    def put_card(self, table: Table) -> None:
        """ Asks and handles which card to put on given table """

        card = questionary.select(
                f"{self.name}: card to put on table: ",
                self.plr_cards
        ).ask()

        self.plr_cards.remove(card)
        table.table_cards.append(card)


    def capture_left_on_table(self, cards: list[str]) -> None:
        if not self.is_table_captures: return

        for card in cards:
            if card not in self.table_captures:
                self.table_captures.append(card)

    def capture_to_hand(self, cards: list[str]) -> None:
        if not self.is_hand_captures: return

        for card in cards:
            if card not in self.plr_cards:
                self.plr_cards.append(card)


    def debug_plr(self) -> None:
        """ Logs card amount and cards """

        print(f"{self.name} card amount: {len(self.plr_cards)}")
        print(f"{self.name} cards: {", ".join(self.plr_cards)}")
        print("")


@dataclass
class Go_Fish:
    """
    This version gives a max of one card per rank match

    -----
    Missing:
    Player new hand amount int handling
    Set handling
    Win / lose state handling
    
    -----
    Creates both a deck and a table on init
    Debug go fish with existing class method or using the instance vars
    """

    def __post_init__(self) -> None:
        self.deck = Cards()
        self.table = Table()

    def __inv_is_hand_captures(self, players: list[Player]) -> bool:
        for plr in players:
            if not plr.is_hand_captures:
                error("Cannot play Go Fish with hand captures off!")
                return True
            else:
                return False
        else: 
            return False


    def __clear_output(self) -> None:
        visible_logs_delay: int = 3

        print("Clearing output to prevent cheating...")
        sleep(visible_logs_delay)

        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")


    def game_loop(self, players: list[Player]) -> None:
        """
        Blocks a non-matching rank selection when you have matches available

        -----
        Errors, if is hand captures is False for given players
        Errors, if card count for deck is invalid
        """

        if self.__inv_is_hand_captures(players): return

        while True:
            if self.deck.inv_deck_count():
                break

            self.__clear_output()

            for plr in players:
                if len(plr.plr_cards) > 0:
                    wish_card = questionary.select(
                            "Ask for a card rank:",
                            plr.plr_cards
                    ).ask()

                    other_players: list[Player] = [p for p in players if p != plr]
                    other_players_name: list[str] = []

                    for other_plr in other_players:
                        other_players_name.append(other_plr.name)

                    selected_plr_name = questionary.select(
                            "Select a player to ask:",
                            other_players_name
                    ).ask()

                    selected_plr_class: Player

                    for other_plr in other_players:
                        if selected_plr_name == other_plr.name:
                            selected_plr_class = other_plr

                    wish_rank: str = emoji.replace_emoji(wish_card, "")
                    match_found: bool = False

                    for card in selected_plr_class.plr_cards:
                        card_rank = emoji.replace_emoji(card, "")

                        if wish_rank == card_rank:
                            match_found = True
                            break
                    
                    if not match_found:
                        print("Fish!")
                        sleep(3)

                        new_card: str = self.deck.draw_card()
                        plr.plr_cards.append(new_card)

                        print(f"You pulled: {new_card}")
                        self.__clear_output()
                    else:
                        self.__clear_output()

                        # block a non-matching rank selection
                        while True:
                            if wish_rank != matching_rank:
                                answer_from_other_plr = questionary.select(
                                        f"Select a card to give for matching card rank: {wish_card}",
                                        selected_plr_class.plr_cards
                                ).ask()

                                matching_rank: str = emoji.replace_emoji(
                                        answer_from_other_plr,
                                        ""
                                )

                                if wish_rank == matching_rank:
                                    print(f"{selected_plr_name} gave you: {answer_from_other_plr}")
                                    plr.capture_to_hand([answer_from_other_plr])
                                    break
