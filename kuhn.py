import numpy as np
import random

class Node:
    def __init__(self, infoset, num_actions):
        self.infoset_id = infoset
        self.regret_sum = np.zeros(num_actions)
        self.strategy = np.zeros(num_actions)
        self.strategy_sum = np.zeros(num_actions)
        self.num_actions = num_actions
        self.visited_count = 0
        self.util_sum = 0

    def get_strategy(self):
        normalizing_sum = 0
        for a in range(self.num_actions):
            if self.regret_sum[a] > 0:
                self.strategy[a] = self.regret_sum[a]
            else:
                self.strategy[a] = 0
            normalizing_sum += self.strategy[a]

        for a in range(self.num_actions):
            if normalizing_sum > 0:
                self.strategy[a] /= normalizing_sum
            else:
                self.strategy[a] = 1.0 / self.num_actions

        return self.strategy

    def get_average_strategy(self):
        avg_strategy = np.zeros(self.num_actions)
        normalizing_sum = 0

        for a in range(self.num_actions):
            normalizing_sum += self.strategy_sum[a]
        for a in range(self.num_actions):
            if normalizing_sum > 0:
                avg_strategy[a] = self.strategy_sum[a] / normalizing_sum
            else:
                avg_strategy[a] = 1.0 / self.num_actions

        return avg_strategy

    def pretty_print(self):
        strat_str = list(
            map(lambda s: "{0:.4f}".format(s), self.get_average_strategy())
        )
        print(
            "history:{0}, avgStrat:{1}, count:{2}, util_sum:{3:.0f}, util:{4:.4f}".format(
                self.infoset_id,
                strat_str,
                self.visited_count,
                self.util_sum,
                self.util_sum / self.visited_count,
            )
        )


class KuhnCFR:
    def __init__(self, iterations, decksize):
        self.nbets = 2
        self.iterations = iterations
        self.decksize = decksize
        self.cards = np.arange(decksize)
        self.bet_options = 2  # he hardcodes this everywhere, don't trust
        self.nodes = {}

    def cfr_iterations_external(self):
        util = np.zeros(2)
        for t in range(1, self.iterations + 1):
            for i in range(2):
                random.shuffle(self.cards)
                util[i] += self.external_cfr(self.cards[:2], [], 2, 0, i, t)
        print("Average game value: {}".format(util[0] / (self.iterations)))
        for i in sorted(self.nodes):
            self.nodes[i].pretty_print()

    def external_cfr(self, cards, history, pot, nodes_touched, traversing_player, t):
        plays = len(history)
        acting_player = plays % 2
        opponent_player = 1 - acting_player
        if plays >= 2:
            if history[-1] == 0 and history[-2] == 1:  # bet fold
                if acting_player == traversing_player:
                    return 1
                else:
                    return -1
            if (history[-1] == 0 and history[-2] == 0) or (
                history[-1] == 1 and history[-2] == 1
            ):  # check check or bet call, go to showdown
                if acting_player == traversing_player:
                    if cards[acting_player] > cards[opponent_player]:
                        return pot / 2
                    else:
                        return -pot / 2
                else:
                    if cards[acting_player] > cards[opponent_player]:
                        return -pot / 2
                    else:
                        return pot / 2

        infoset = str(cards[acting_player]) + str(history)
        if infoset not in self.nodes:
            self.nodes[infoset] = Node(infoset, self.bet_options)

        nodes_touched += 1

        if acting_player == traversing_player:
            util = np.zeros(self.bet_options)  # 2 actions
            node_util = 0
            strategy = self.nodes[infoset].get_strategy()
            for a in range(self.bet_options):
                next_history = history + [a]
                util[a] = self.external_cfr(
                    cards, next_history, pot + a, nodes_touched, traversing_player, t
                )
                node_util += strategy[a] * util[a]

            for a in range(self.bet_options):
                regret = util[a] - node_util
                self.nodes[infoset].regret_sum[a] += regret
            self.nodes[infoset].util_sum += node_util
            self.nodes[infoset].visited_count += 1
            return node_util

        else:  # acting_player != traversing_player
            strategy = self.nodes[infoset].get_strategy()
            util = 0
            if random.random() < strategy[0]:
                next_history = history + [0]
            else:
                next_history = history + [1]
                pot += 1
            util = self.external_cfr(
                cards, next_history, pot, nodes_touched, traversing_player, t
            )
            for a in range(self.bet_options):
                self.nodes[infoset].strategy_sum[a] += strategy[a]
            return util


if __name__ == "__main__":
    # k = KuhnCFR(2000000, 10)
    k = KuhnCFR(10000, 3)
    k.cfr_iterations_external()
