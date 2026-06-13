import questionary

from modules.classes import *


def main() -> None:
    #scopa_game = Scopa()
    #scopa_game.debug_cards()

    go_fish_game = Go_Fish()

    plr_1_name = questionary.text("Player 1: Type your name: ", default="Player 1").ask()
    plr_2_name = questionary.text("Player 2: Type your name: ", default="Player 2").ask()

    player_1 = Player(
        name=plr_1_name,
        deck=go_fish_game.deck,
        new_hand_amount=7,
        is_hand_captures=True)
    #player_1.debug_plr()

    """ player_1.plr_cards = [
        "❤️A",
        "♠️A",
        "♣️A",
        "♦️A"
    ] """

    player_2 = Player(
        name=plr_2_name,
        deck=go_fish_game.deck,
        new_hand_amount=7,
        is_hand_captures=True)
    #player_2.debug_plr()

    #scopa_game.game_loop(
        #players=[player_1, player_2]
    #)

    #scopa_deck.debug_scopa(players=[player_1, player_2])

    #scopa_winner: int | None = max(len(player_1.table_captures), len(player_2.table_captures)) or None
    #print("Scopa winner:", scopa_winner)

    #go_fish_game.__handle_completed_sets(players=[player_1, player_2])

    go_fish_game.game_loop(players=[player_1, player_2])


if __name__ == "__main__":
    main()
