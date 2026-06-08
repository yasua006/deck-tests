import random
from dataclasses import dataclass

from personal_logging.main import warn


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

    def shuffle_cards(self) -> None:
        random.shuffle(self.deck)

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

    rnd_card_amount: int = 4
    """ The card amount to put on the table using the deck """

    def __post_init__(self) -> None:
        super().__post_init__()
        self.table_cards: list[str] = []
        self.put_cards_on_table()

    def put_cards_on_table(self) -> None:
        self.table_cards = random.choices(self.deck_list, k=self.rnd_card_amount)

    def debug_table_cards(self) -> None:
        print(f"Table cards: {', '.join(self.table_cards)}")


@dataclass
class Player(Cards):
    """
    New hand on init
    Debug the player with existing class method or using the instance vars
    """

    name: str = ""
    card_amount: int = 0
    new_hand_amount: int = 3

    def __post_init__(self) -> None:
        super().__post_init__()
        self.plr_cards: list[str] = []
        self.new_hand()

    def new_hand(self) -> None:
        self.card_amount += self.new_hand_amount
        self.plr_cards.append(random.choices(self.deck_list, k=self.new_hand_amount))

    def debug_plr(self) -> None:
        print(f"{self.name} card amount: {self.card_amount}")
        print(f"{self.name} cards: {self.plr_cards}")
        

def main() -> None:
    cards = Cards()
    cards.debug_cards()

    table_cards = Table()
    table_cards.debug_table_cards()
    #print(table_cards)

    player_1 = Player("Player 1")
    player_1.debug_plr()

    player_2 = Player("Player 2")
    player_2.debug_plr()

if __name__ == "__main__":
    main()
