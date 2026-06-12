from modules.classes import *


def main() -> None:
    scopa_deck = Scopa()
    #scopa_deck.debug_cards()

    table = Table("Test")
    #print(table_cards)

    player_1 = Player("Player 1", is_table_captures=True)
    #player_1.debug_plr()

    player_2 = Player("Player 2", is_table_captures=True)
    #player_2.debug_plr()

    scopa_deck.game_loop(
        players=[player_1, player_2],
        table=table
    )

    scopa_deck.debug_scopa(players=[player_1, player_2])

    scopa_winner: int | None = max(len(player_1.table_captures), len(player_2.table_captures)) or None
    print("Scopa winner:", scopa_winner)


if __name__ == "__main__":
    main()
