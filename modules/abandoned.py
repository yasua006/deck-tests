@dataclass
class Scopa:
    """
    Missing:
    All capture methods handling 
    Win / lose state handling

    -----
    Creates both a deck and a table on init
    Puts cards on the table on init
    Debug scopa with existing class methods or using the instance vars

    -----
    Abandon reasons:
    Start smaller - go fish game
    Multi capture handling logic
    """

    def __post_init__(self) -> None:
        self.deck = Cards()
        self.table = Table()

        for card in self.deck.deck_list[:]: # Init workaround
            if ("8" in card or "9" in card or "10" in card):
                #print("Removing:", card)
                self.deck.deck_list.remove(card)

        self.put_cards_on_table()

    def put_cards_on_table(self) -> None:
        for _ in range(self.table.rnd_card_amount):
            self.table.table_cards.append(self.deck.draw_card())


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

        if self.deck.inv_deck_count(): return

        for plr in players:
            if self.inv_plr_card_count(plr): return

            plr.new_hand()

    
    def game_loop(self, players: list[Player]) -> None:
        """
        Errors, if card count for deck is invalid
        """

        while True:
            if self.deck.inv_deck_count():
                break

            self.table.show_table_cards()

            for plr in players:
                if len(plr.plr_cards) > 0:
                    plr.put_card(self.table) 
                else:
                    self.new_round(players)

    def debug_scopa(self, players: list[Player]) -> None:
        """ Logs player captures from given players """

        for plr in players:
            print(f"{plr.name} captures: {plr.table_captures}")
