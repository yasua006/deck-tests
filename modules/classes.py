import random
from dataclasses import dataclass

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
            error("Cannot start a new scopa round! Invalid or low card count for deck!")
            return True

        return False


    def shuffle_cards(self) -> None:
        random.shuffle(self.deck_list)

    def draw_card(self) -> str:
        if self.inv_deck_count(): return "Cannot draw a card!"

        """ Draws a card from backwards (face down deck) """
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
class Table(Cards):
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
        super().__post_init__()
        self.table_cards: list[str] = []
        self.put_cards_on_table()

    def put_cards_on_table(self) -> None:
        for _ in range(self.rnd_card_amount):
            self.table_cards.append(self.draw_card())

    def show_table_cards(self) -> None:
        print(f"\nTable cards: {', '.join(self.table_cards)}\n")


@dataclass
class Player(Cards):
    """
    New hand on init
    Captures are disabled by default
    Debug the player with existing class method or using the instance vars

    -----
    Errors, if both capture booleans are set to True
    """

    name: str = ""

    new_hand_amount: int = 3

    is_table_captures: bool = False
    """ Allows captures left on the table face down """
    is_hand_captures: bool = False
    """ Allows captures incrementing player card(s)"""

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.is_table_captures and self.is_hand_captures:
            error("Player cannot capture both ways: table and hand!")
            return

        self.plr_cards: list[str] = []

        if self.is_table_captures:
            self.table_captures = []

        self.new_hand()

    def new_hand(self) -> None:
        for _ in range(self.new_hand_amount):
            self.plr_cards.append(self.draw_card())

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


class Scopa(Cards):
    """
    Debug scopa with existing class methods or using the instance vars
    """

    def __post_init__(self) -> None:
        super().__post_init__() 
        
        for card in self.deck_list[:]: # Init workaround
            if ("8" in card or "9" in card or "10" in card):
                #print("Removing:", card)
                self.deck_list.remove(card)


    def inv_plr_card_count(self, plr: Player) -> bool:
        if len(plr.plr_cards) > 0:
            error(f"Cannot start a new scopa round! Non-zero card count for {plr.name}!")
            return True

        return False

    def new_round(self, players: list[Player]) -> None:
        """
        Starts a new round (a new hand to each player given)

        -----
        Errors, if you cannot start a new scopa round
        """

        if self.inv_deck_count(): return

        for plr in players:
            if self.inv_plr_card_count(plr): return

            plr.new_hand()

    
    def game_loop(self, players: list[Player], table: Table) -> None:
        """ table - The same table players play at """

        #while not self.inv_deck_count():

        for _ in range(len(self.deck_list)):
            #warn(f"Attempt: {i}")

            table.show_table_cards()

            for plr in players:
                if len(plr.plr_cards) > 0:
                    plr.put_card(table) 
                else:
                    self.new_round(players)

    def debug_scopa(self, players: list[Player]) -> None:
        """ Logs player captures from given players """

        for plr in players:
            print(f"{plr.name} captures: {plr.table_captures}")
