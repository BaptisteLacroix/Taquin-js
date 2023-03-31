# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Jeremy Hummel
# 02/11/14
# CMPSCI 383

import copy
import random
import re

from flask import request, Flask, jsonify
from flask_cors import CORS


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg


class EightPuzzle:

    def __init__(self, string, size=3):
        """
        It takes a string as input, and if the string is formatted correctly,
        it creates a new Puzzle object with the state
        of the puzzle set to the state described by the string

        :param str: The string that is being passed in
        """
        # pttn = re.compile("(\d)\s(\d)\s(\d)\s(\d)\s(\d)\s(\d)\s(\d)\s(\d)\s(\d)") for 3x3
        # result = pttn.match(string)
        # do the pattern dynamically
        self.size = size
        pttn = re.compile("(\d{1,2})")
        for i in range(self.size * self.size - 1):
            if i > 8:
                pttn = re.compile(pttn.pattern + "\s(\d{1,2})")
            else:
                pttn = re.compile(pttn.pattern + "\s(\d{1,2})")

        result = pttn.match(string)

        if result is not None:
            s = result.groups()
            # self.state = [[int(s[0]), int(s[1]), int(s[2])], [int(s[3]), int(s[4]), int(s[5])], [int(s[6]), int(s[7]), int(s[8])]]
            # create the state dynamically
            self.state = []
            for i in range(size):
                row = []
                for j in range(size):
                    row.append(int(s[i * size + j]))
                self.state.append(row)
        else:
            raise InputError("Improperly formatted 8-puzzle")

    def __str__(self):
        """
        The function takes in a state and returns a string representation of the state
        :return: The string representation of the state of the board.
        """

        s = ''
        for i in range(0, self.size):
            for j in range(0, self.size):
                s += str(self.state[i][j]) + ' '
        return s

    # def __str__(self):
    #    s = ''
    #    for i in range (0,3):
    #        for j in range (0,3):
    #            s += str(self.state[i][j]) + ' '
    #        s += '\n'
    #    return s

    def __eq__(self, other):
        """
        If the other object is of the same type as this object, then compare the two
        objects' dictionaries. Otherwise,
        return False

        :param other: The object to compare to
        :return: The __eq__ method is being returned.
        """
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """
        If the two objects are not equal, then return True

        :param other: The other object to compare to
        :return: The return value is a boolean value.
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        It converts the state of the puzzle into a unique integer
        :return: The unique id of the state.
        """
        uid = 0
        mult = 1
        for i in range(0, self.size):
            for j in range(0, self.size):
                uid += self.state[i][j] * mult
                mult *= self.size * self.size
        return uid

    def tile_switches_remaining(self, goal):
        """
        It counts the number of tiles that are not in the goal state.

        :param goal: The goal state of the puzzle
        :return: The number of tiles that are not in the correct position.
        """
        sum = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.state[i][j] != goal.state[i][j]:
                    sum += 1
        return sum

    def manhatten_distance(self, goal):
        """
        For each tile in the current state, find the tile in the goal state that matches it,
        and add the manhatten distance
        between the two tiles to the sum

        :param goal: The goal state of the puzzle
        :return: The sum of the manhatten distances of each tile from its goal position.
        """
        sum = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                tile = self.state[i][j]
                for m in range(0, self.size):
                    for n in range(0, self.size):
                        if tile == goal.state[m][n]:
                            sum += abs(i - m) + abs(j - n)
        return sum

    def neighbors(self):
        """
        For each possible move, create a new state by copying the current state,
        then make the move, and add the new state
        to the list of neighbors
        :return: A list of tuples. Each tuple contains a copy of the current state
        and a string representing the direction
        of the move.

        list = []
        idx = self.get_blank_index()
        x = idx[0]
        y = idx[1]
        if x > 0:
            r = copy.deepcopy(self)
            r.state[y][x] = r.state[y][x - 1]
            r.state[y][x - 1] = 0
            list.append((r, 'r'))
        if x < 2:
            l = copy.deepcopy(self)
            l.state[y][x] = l.state[y][x + 1]
            l.state[y][x + 1] = 0
            list.append((l, 'l'))
        if y > 0:
            d = copy.deepcopy(self)
            d.state[y][x] = d.state[y - 1][x]
            d.state[y - 1][x] = 0
            list.append((d, 'd'))
        if y < 2:
            u = copy.deepcopy(self)
            u.state[y][x] = u.state[y + 1][x]
            u.state[y + 1][x] = 0
            list.append((u, 'u'))
        return list
        """
        list = []
        idx = self.get_blank_index()
        x = idx[0]
        y = idx[1]
        size = len(self.state)
        if x > 0:
            r = copy.deepcopy(self)
            r.state[y][x] = r.state[y][x - 1]
            r.state[y][x - 1] = 0
            list.append((r, 'r'))
        if x < (size - 1):
            l = copy.deepcopy(self)
            l.state[y][x] = l.state[y][x + 1]
            l.state[y][x + 1] = 0
            list.append((l, 'l'))
        if y > 0:
            d = copy.deepcopy(self)
            d.state[y][x] = d.state[y - 1][x]
            d.state[y - 1][x] = 0
            list.append((d, 'd'))
        if y < (size - 1):
            u = copy.deepcopy(self)
            u.state[y][x] = u.state[y + 1][x]
            u.state[y + 1][x] = 0
            list.append((u, 'u'))
        return list

    def get_blank_index(self):
        """
        It returns the x and y coordinates of the blank tile in the puzzle
        :return: The x and y coordinates of the blank space.
        """
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.state[i][j] == 0:
                    x = j
                    y = i
        return x, y

    def a_star(self, goal, heuristic, output):
        """
        > We start with a set of nodes to explore (open_set) and a set of nodes we have already explored
        (closed_set). We
        explore the node in open_set with the lowest f_score (the sum of the cost to get there and the
        heuristic cost to get
        to the goal). We add this node to the closed_set and remove it from the open_set. We then add
         all of its neighbors
        to the open_set if they are not already in the closed_set

        :param goal: the goal configuration
        :param heuristic: a function that takes two states and returns a number
        :param output: a function that takes the start node, the dictionary of came_from, and the goal
        node, and returns the
        path from start to goal
        :return: The path from the start to the goal.
        """
        closed_set = set()
        open_set = {self}
        came_from = {}

        g_score = {self: 0}
        f_score = {self: g_score[self] + heuristic(self, goal)}
        count = 0  # combien de configuration a-t-on développé ?
        while len(open_set) != 0:
            current = None
            for node in open_set:
                if current is None or f_score[node] < f_score[current]:
                    current = node
            if current == goal:
                # clear memory like garbage collector
                del closed_set
                return output(self, came_from, current)

            count += 1
            if (count % 200 == 0):
                print(count, len(closed_set), "Developing: ", current)
            open_set.remove(current)
            closed_set.add(current)
            #             print ("Closed set:")
            #             for p in closed_set:
            #                 print (p)
            for n in current.neighbors():
                neighbor = n[0]
                #                print ("Neighbor:\n",neighbor)
                if neighbor in closed_set:
                    #                    print ("Current:\n",current)
                    #                    print ("Neighbor:\n",neighbor)
                    continue
                tentative_g_score = g_score[current] + 1

                if neighbor not in open_set or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = (current, n[1])
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    if neighbor not in open_set:
                        open_set.add(neighbor)
        #                        print ("->", neighbor)
        # clear memory like garbage collector
        del closed_set
        return "nil"

    def action_sequence(self, came_from, current_node):
        """
        Given a dictionary of nodes and their parents, and a current node, return the sequence of
        actions that would take you from the start node to the current node

        :param came_from: a dictionary that maps a node to its parent node
        :param current_node: the current node we're at
        :return: The action sequence is being returned.
        """
        goal = current_node
        return self.action_sequence_helper(came_from, current_node, goal)

    def action_sequence_helper(self, came_from, current_node, goal):
        """
        The function takes in a dictionary of nodes and their parents, a current node, and a goal node.
        It returns a string of actions that will take you from the current node to the goal node

        :param came_from: a dictionary that maps a node to a tuple of (parent node, action)
        :param current_node: the current node we're looking at
        :param goal: the goal node
        :return: The action sequence is being returned.
        """
        delineator = ","
        if current_node == goal:
            delineator = ""
        if current_node in came_from:
            p = self.action_sequence_helper(came_from, came_from[current_node][0], goal)
            p += came_from[current_node][1] + delineator
            return p
        else:
            return ""

    def state_transition(self, came_from, current_node):
        """
        Given a dictionary of nodes and their parents, and a current node, return the path from the
        current node to the goal

        :param came_from: a dictionary that maps a node to its parent node
        :param current_node: the current node we're looking at
        :return: The path from the start to the goal.
        """
        goal = current_node
        return self.state_transition_helper(came_from, current_node, goal)

    def state_transition_helper(self, came_from, current_node, goal):
        """
        It recursively traverses the came_from dictionary, starting at the goal node, and returns
        a string of the path from the goal node to the start node

        :param came_from: a dictionary that maps a node to a tuple of (parent node, action)
        :param current_node: the current node we're looking at
        :param goal: The goal node
        :return: The path from the start to the goal.
        """
        delineator = "\n"
        if current_node == goal:
            delineator = ""
        if current_node in came_from:
            p = self.state_transition_helper(came_from, came_from[current_node][0], goal)
            p += str(current_node) + delineator
            return p
        else:
            return str(current_node) + delineator


app = Flask(__name__)
CORS(app)  # add cors so you don't get a cors error


@app.route('/a_star', methods=['GET', 'POST'])
def a_star():
    print("a_star")
    url = request.get_data  # = <bound method Request.get_data of <Request 'http://localhost:5000/a_star?json%5BstringInitial%5D=%224%201%203%205%202%208%206%207%200%22&json%5Bgoal%5D=%220%201%202%203%204%205%206%207%208%22' [GET]>>
    # transfomr url as string
    url = str(url)
    # split the string to get the stringInitial and the goal
    url = url.split("&")
    # get the stringInitial and delete all the %20
    initial = url[0].split("=")[1].replace("%20", " ").replace("%22", "")
    # get the goal and delete all the %20 Replace all values different from 0-9 and a-z
    goal = url[1].split("=")[1].replace("%20", " ").replace("%22", "")
    size = int(url[2].split("=")[1].replace("%22", "").replace("' [GET]>>", ""))


    print("initial: ", initial)
    print("goal: ", goal)
    # create the initial state
    initial = EightPuzzle(initial, size)
    goal = EightPuzzle(goal, size)

    heuristic = EightPuzzle.manhatten_distance
    output = EightPuzzle.action_sequence
    result = initial.a_star(goal, heuristic, output)
    print(result)
    return jsonify(result)


@app.route('/generate_puzzle', methods=['GET', 'POST'])
def generate_puzzle() -> (str, str):
    """
    Génère un état initial au hasard et un but au hasard, en vérifiant que l'état initial est résolvable.
    :return:
    """
    # code pour 50 permutations aléatoires
    size = int(str(request.get_data).split("=")[1].replace("%22", "").replace("' [GET]>>", ""))

    intitialString = ""
    for i in range(size * size):
        intitialString += str(i) + " "
    initialString = intitialString[:-1]

    initial, goal = EightPuzzle(initialString, size), EightPuzzle(initialString, size)
    for _ in range(50):
        initial = random.choice(initial.neighbors())[0]
    return jsonify(initial.__str__(), goal.__str__())


if __name__ == '__main__':
    app.run(debug=True)
