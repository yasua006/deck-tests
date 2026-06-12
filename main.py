from modules.classes import *


def main() -> None:
    scopa_game = Scopa()
    #scopa_game.debug_cards()

    player_1 = Player(
        name="Player 1",
        deck=scopa_game.deck,
        is_table_captures=True)
    #player_1.debug_plr()

    player_2 = Player(
        name="Player 2",
        deck=scopa_game.deck,
        is_table_captures=True)
    #player_2.debug_plr()

    scopa_game.game_loop(
        players=[player_1, player_2]
    )

    #scopa_deck.debug_scopa(players=[player_1, player_2])

    #scopa_winner: int | None = max(len(player_1.table_captures), len(player_2.table_captures)) or None
    #print("Scopa winner:", scopa_winner)


if __name__ == "__main__":
    main()
