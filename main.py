from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ObjectProperty


class AjuaRoot(BoxLayout):
    p1cup1 = NumericProperty()
    p1cup2 = NumericProperty()
    p1cup3 = NumericProperty()
    p1cup4 = NumericProperty()
    p1cup5 = NumericProperty()
    p1cup6 = NumericProperty()
    p1home = NumericProperty()

    p2cup1 = NumericProperty()
    p2cup2 = NumericProperty()
    p2cup3 = NumericProperty()
    p2cup4 = NumericProperty()
    p2cup5 = NumericProperty()
    p2cup6 = NumericProperty()
    p2home = NumericProperty()

    p1btn1 = ObjectProperty()
    p1btn2 = ObjectProperty()
    p1btn3 = ObjectProperty()
    p1btn4 = ObjectProperty()
    p1btn5 = ObjectProperty()
    p1btn6 = ObjectProperty()

    p2btn1 = ObjectProperty()
    p2btn2 = ObjectProperty()
    p2btn3 = ObjectProperty()
    p2btn4 = ObjectProperty()
    p2btn5 = ObjectProperty()
    p2btn6 = ObjectProperty()

    start_player = "p1"
    current_player = start_player

    def __init__(self, **kwargs):
        super(AjuaRoot, self).__init__(**kwargs)
        self.p1cup1 = 4
        self.p1cup2 = 4
        self.p1cup3 = 4
        self.p1cup4 = 4
        self.p1cup5 = 4
        self.p1cup6 = 4
        self.p1home = 0

        self.p2cup1 = 4
        self.p2cup2 = 4
        self.p2cup3 = 4
        self.p2cup4 = 4
        self.p2cup5 = 4
        self.p2cup6 = 4
        self.p2home = 0

        self.deactivate_opponent()

    def player_selection(self, current_player, selected_cup):
        if current_player is 1:
            player = "p1"
            opponent = "p2"
        else:
            player = "p2"
            opponent = "p1"

        no_of_stones_in_hand = getattr(self, player + "cup" + str(selected_cup))
        starting_cup = selected_cup + 1
        ending_cup = selected_cup + no_of_stones_in_hand
        # Set selected cup to zero
        setattr(self, player + "cup" + str(selected_cup), 0)
        print "\nNEW ROUND\n"
        print "Picked from Cup: {}".format(selected_cup)
        self.make_player_move(player, opponent, starting_cup, ending_cup, no_of_stones_in_hand)

    def make_player_move(self, player, opponent, starting_cup, ending_cup, no_of_stones_in_hand):
        if no_of_stones_in_hand is not 0:
            remaining_stones_in_hand = no_of_stones_in_hand

            print "Starting Cup: {}".format(starting_cup)
            print "No of Stones: {}".format(no_of_stones_in_hand)
            print "Ending Cup: {}\n".format(ending_cup)

            # PLAYERS SIDE
            for i in xrange(starting_cup, 7):
                setattr(self, player + "cup" + str(i), getattr(self, player + "cup" + str(i)) + 1)
                remaining_stones_in_hand -= 1
                if remaining_stones_in_hand is 0:
                    # Check for capture
                    no_of_stones_in_ending_cup = getattr(self, player + "cup" + str(i))
                    self.is_capture(i, no_of_stones_in_ending_cup, player, opponent)
                    # Check if Game is over or switch players
                    if self.is_game_over(player, opponent):
                        self.find_winner(player, opponent)
                    else:
                        self.switch_players(opponent)
                    break

            # PLAYERS AJUA
            if remaining_stones_in_hand is not 0:
                # PUT A STONE HOME
                setattr(self, player + "home", getattr(self, player + "home") + 1)
                remaining_stones_in_hand -= 1
                if remaining_stones_in_hand is 0:
                    # Check if Game is over or Get a free turn
                    if self.is_game_over(player, opponent):
                        self.find_winner(player, opponent)
                    else:
                        print "FREE TURN"

            # OPPONENTS SIDE
            if remaining_stones_in_hand is not 0:
                for i in xrange(1, 7):
                    setattr(self, opponent + "cup" + str(i), getattr(self, opponent + "cup" + str(i)) + 1)
                    remaining_stones_in_hand -= 1
                    if remaining_stones_in_hand is 0:
                        # Check if Game is over or switch players
                        if self.is_game_over(player, opponent):
                            self.find_winner(player, opponent)
                        else:
                            self.switch_players(opponent)
                        break

            if ending_cup > 13:
                new_ending_cup = ending_cup - 13
                self.make_player_move(player, opponent, 1, new_ending_cup, remaining_stones_in_hand)

                # self.deactivate_player(player)

    def is_capture(self, ending_cup, no_of_stones_in_ending_cup, player, opponent):
        # IF You drop it into a cup that was previously empty AND the cup is on your side == CAPTURED
        if no_of_stones_in_ending_cup is 1:
            if ending_cup is 1:
                capture_cup = 6
            elif ending_cup is 2:
                capture_cup = 5
            elif ending_cup is 3:
                capture_cup = 4
            elif ending_cup is 4:
                capture_cup = 3
            elif ending_cup is 5:
                capture_cup = 2
            elif ending_cup is 6:
                capture_cup = 1

            no_of_stones_to_be_captured = getattr(self, opponent + "cup" + str(capture_cup))
            if no_of_stones_to_be_captured is not 0:
                # Set ending cup to zero
                setattr(self, player + "cup" + str(ending_cup), 0)
                # Set selected cup to zero
                setattr(self, opponent + "cup" + str(capture_cup), 0)
                # Increase player home by capture
                setattr(self, player + "home", getattr(self, player + "home") + (no_of_stones_to_be_captured + 1))
                print "CAPTURED"

    def is_game_over(self, player, opponent):
        # One player has no more stones on their side
        no_of_stones_on_player_side = 0
        no_of_stones_on_opponent_side = 0
        for i in xrange(1, 7):
            no_of_stones_on_player_side += getattr(self, player + "cup" + str(i))
            no_of_stones_on_opponent_side += getattr(self, opponent + "cup" + str(i))
        if no_of_stones_on_player_side is 0 or no_of_stones_on_opponent_side is 0:
            return True
        else:
            return False

    def find_winner(self, player, opponent):
        # Opponent takes all stones on his side and places in their Ajua
        # Person with more stones in their Ajua is the winner
        no_of_stones_on_player_side = 0
        no_of_stones_on_opponent_side = 0
        for i in xrange(1, 7):
            no_of_stones_on_player_side += getattr(self, player + "cup" + str(i))
            no_of_stones_on_opponent_side += getattr(self, opponent + "cup" + str(i))

        if no_of_stones_on_player_side is 0:
            for i in xrange(1, 7):
                # Set this cup to zero
                setattr(self, opponent + "cup" + str(i), 0)
            # Put all remaining stones in opponents Ajua
            setattr(self, opponent + "home", getattr(self, opponent + "home") + no_of_stones_on_opponent_side)
        elif no_of_stones_on_opponent_side is 0:
            for i in xrange(1, 7):
                # Set this cup to zero
                setattr(self, player + "cup" + str(i), 0)
            # Put all remaining stones in players Ajua
            setattr(self, player + "home", getattr(self, player + "home") + no_of_stones_on_player_side)

        no_of_stones_on_player_ajua = getattr(self, player + "home")
        no_of_stones_on_opponent_ajua = getattr(self, opponent + "home")

        if no_of_stones_on_player_ajua > no_of_stones_on_opponent_ajua:
            winner = player
        else:
            winner = opponent

        print "WINNER: {}".format(winner)

    def switch_players(self, opponent):
        self.current_player = opponent
        self.deactivate_opponent()
        print "{} TURN".format(opponent)

    def deactivate_opponent(self):
        if self.current_player is "p1":
            self.p1btn1.disabled = False
            self.p1btn2.disabled = False
            self.p1btn3.disabled = False
            self.p1btn4.disabled = False
            self.p1btn5.disabled = False
            self.p1btn6.disabled = False

            self.p2btn1.disabled = True
            self.p2btn2.disabled = True
            self.p2btn3.disabled = True
            self.p2btn4.disabled = True
            self.p2btn5.disabled = True
            self.p2btn6.disabled = True
        elif self.current_player is "p2":
            self.p1btn1.disabled = True
            self.p1btn2.disabled = True
            self.p1btn3.disabled = True
            self.p1btn4.disabled = True
            self.p1btn5.disabled = True
            self.p1btn6.disabled = True

            self.p2btn1.disabled = False
            self.p2btn2.disabled = False
            self.p2btn3.disabled = False
            self.p2btn4.disabled = False
            self.p2btn5.disabled = False
            self.p2btn6.disabled = False


class AjuaApp(App):
    pass


if __name__ == '__main__':
    AjuaApp().run()
