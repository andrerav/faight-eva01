from util.Ticker import Ticker
from util.States import States
from util.Map import Map
from util.Message import Message
from util.Message import Player
import random as r

class AI(object):
    def __init__(self):
        self.ticker = Ticker()
        self.states = States(self.ticker)
        self.message = Message()
        self.map = Map()
        self.you = Player()
        self.enemy = Player()
        self.history = MoveHistory(length=50, history=[])

    def setup(self,info):
        self.message.parse_message(info)
        self.map = self.message.map
        self.map.load_json_map()
        self.you = self.message.you

    def reset_for_next_round(self):
        self.you = Player()
        self.enemy = Player()
        self.map.reset_map()
        self.ticker.reset()

    def update(self, info):
        self.ticker.tick()
        self.message.parse_message(info)
        self.you = self.message.you
        self.possible_moves = self.map.get_neighbours_of(self.you.pos)
        self.enemy = self.message.enemy
        self.__update_danger()
        self.map.update_content(self.message,[self.you.pos,self.enemy.pos])

    def __update_danger(self):
        if self.you.pos in self.map.super_pellets_positions:
            self.ticker.start_you_are_dangerous_ticker()
        if self.enemy.pos in self.map.super_pellets_positions:
            self.ticker.start_other_is_dangerous_ticker()

    def move(self):
        move = self.__get_the_move(self.map)
        return move

    def __get_the_move(self, map):
        avail_pellet_moves = []
        avail_new_moves = []
        avail_old_moves = []

        for possible_move in self.possible_moves:

            # Just do this move if it's a super pellet
            if possible_move in map.super_pellets_positions:
                return map.get_move_between(self.you.pos, possible_move)

            # Record possible pellet move
            elif possible_move in map.pellet_positions:
                avail_pellet_moves.append(possible_move)

            # Track old moves
            if self.history.contains(possible_move):
                avail_old_moves.append(possible_move)
            else: avail_new_moves.append(possible_move)

        if len(avail_pellet_moves) > 0: move = r.choice(avail_pellet_moves)
        else: move = r.choice(avail_new_moves) if len(avail_new_moves) > 0 else r.choice(avail_old_moves)

        # Chase super pellets
        for supahpelletz in map.super_pellets_positions:
            moves_to_supapellet = map.get_breadth_first_path(self.you.pos, supahpelletz)
            if (len(moves_to_supapellet) < 10):
                move = moves_to_supapellet[0]
                print("Chasing a super pellet!")
                break

        # Chase enemy if dangerous
        if (self.you.is_dangerous and not self.enemy.is_dangerous):
            move = map.get_breadth_first_path(self.you.pos, self.enemy.pos)[0]
            print("I'm dangerous!")

        self.history.add(move)

        return map.get_move_between(self.you.pos, move)

class MoveHistory(object):
    def __init__(self,length=50, history=[]):
        self.__history = history
        self.limit = length

    def add(self, pos):
        if not self.contains(pos):
            self.__history.append(pos)
        if len(self.__history) > self.limit:
            del_point = (len(self.__history)) - self.limit
            self.__history = self.__history[del_point:]

    def contains(self, pos):
        return pos in self.__history

    def __str__(self):
        return str(self.__history)