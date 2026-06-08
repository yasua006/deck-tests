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

    def put_cards_on_table(self) -> list[str]:
        self.table_cards = random.choices(self.deck_list, k=self.rnd_card_amount)
        return self.table_cards

    def debug_table_cards(self) -> None:
        print(f"Table cards: {', '.join(self.table_cards)}")


def main() -> None:
    cards = Cards()
    cards.debug_cards()

    table_cards = Table()
    print(table_cards)

if __name__ == "__main__":
    main()
