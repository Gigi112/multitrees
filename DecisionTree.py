import Parameterclass as P


class Node:
    """ base (master) class for nodes """
    def __init__(self, name, cost, utility):
        """
        :param name: name of this node
        :param cost: cost of visiting this node
        :param utility: utility of visiting this node
        """
        self.name = name
        self.cost = cost
        self.utility = utility

    def get_expected_cost(self):
        """ abstract method to be overridden in derived classes
        :returns expected cost of this node """

    def get_expected_utility(self):
        """ abstract method to be overridden in derived classes
        :returns expected utility of this node """


class ChanceNode(Node):

    def __init__(self, name, cost, utility, future_nodes, probs):
        """
        :param name: name of this node
        :param cost: cost of visiting this node
        :param utility: utility of visiting this node
        :param future_nodes: (list) future nodes connected to this node
        :param probs: (list) probability of future nodes
        """

        Node.__init__(self,name, cost, utility)


        self.futureNodes = future_nodes
        self.probs = probs

    def get_expected_cost(self):
        """
        :return: expected cost of this chance node
        E[cost] = (cost of visiting this node)
                  + sum_{i}(probability of future node i)*(E[cost of future node i])
        """

        # expected cost initialized with the cost of visiting the current node
        exp_cost = self.cost

        # go over all future nodes
        i = 0
        for node in self.futureNodes:
            # increment expected cost by
            # (probability of visiting this future node) * (expected cost of this future node)
            exp_cost += self.probs[i]*node.get_expected_cost()
            i += 1

        return exp_cost

    def get_expected_utility(self):
        """
        :return: expected utility of this chance node
        E[utility] = (utility of visiting this node)
                  + sum_{i}(probability of future node i)*(E[utility of future node i])
        """

        # expected utility initialized with the cost of visiting the current node
        exp_utility = self.utility

        # go over all future nodes
        i = 0
        for node in self.futureNodes:
            # increment expected utility by
            # (probability of visiting this future node) * (expected utility of this future node)
            exp_utility += self.probs[i]*node.get_expected_utility()
            i += 1

        return exp_utility


class TerminalNode(Node):

    def __init__(self, name, cost, utility):
        """
        :param name: name of this node
        :param cost: cost of visiting this node
        :param utility: utility of visiting this node
        """

        Node.__init__(self, name, cost, utility)

    def get_expected_cost(self):
        """
        :return: cost of this visiting this terminal node
        """
        return self.cost

    def get_expected_utility(self):
        """
        :return: utility of this visiting this terminal node
        """
        return self.utility


class DecisionNode(Node):

    def __init__(self,name, cost, utility, future_nodes):
        """
        :param name: name of this node
        :param cost: cost of visiting this node
        :param utility: utility of visiting this node
        :param future_nodes: (list) future nodes connected to this node
        (assumes that future nodes can only be chance or terminal nodes)
        """

        Node.__init__(self, name, cost, utility)
        self.futureNode = future_nodes

    def get_expected_costs(self):
        """ returns the expected costs of future nodes
        :return: a dictionary of expected costs of future nodes with node names as dictionary keys
        """

        # a dictionary to store the expected cost of future nodes
        exp_costs = dict()
        # go over all future nodes
        for node in self.futureNode:
            # add the expected cost of this future node to the dictionary
            exp_costs[node.name] = self.cost + node.get_expected_cost()

        return exp_costs

    def get_expected_utilities(self):
        """ returns the expected utilities of future nodes
        :return: a dictionary of expected utilities of future nodes with node names as dictionary keys
        """

        # a dictionary to store the expected cost of future nodes
        exp_utilities = dict()
        # go over all future nodes
        for node in self.futureNode:
            # add the expected cost of this future node to the dictionary
            exp_utilities[node.name] = self.utility + node.get_expected_utility()

        return exp_utilities



#######################
# See figure DT3.png (from the project menu) for the structure of this decision tree
########################
class tree():
    def __init__(self,  id, parameters):
        self.id = id
        self.params = parameters

        # create the terminal nodes
        self.T1 = TerminalNode('Sequelae',parameters.seqcost,parameters.sequtility)
        self.T2 = TerminalNode('No Sequelae', 0, 1)
        self.T3 = TerminalNode('Die', 0, 0)
        self.T4 = TerminalNode('Survive', 0, 1)
        self.T5 = TerminalNode('Die', 0, 0)
        self.T6 = TerminalNode('Sequelae', parameters.seqcost,parameters.sequtility)
        self.T7 = TerminalNode('No Sequelae', 0, 1)
        self.T8 = TerminalNode('Die', 0, 0)
        self.T9 = TerminalNode('Survive', 0, 1)
        self.T10 = TerminalNode('Die', 0, 0)

        self.C3 = ChanceNode('Survive', 0, 0, [self.T1, self.T2], [parameters.prob_seq,(1-parameters.prob_seq)])

        self.C4 = ChanceNode('No hospitalizition', 0, parameters.rsv_nh_u,[self.T4, self.T5], [(1-parameters.probnhpd),parameters.probnhpd])

        self.C7 = ChanceNode('Survive', 0, 0, [self.T6, self.T7], [parameters.prob_seq,(1-parameters.prob_seq)])

        # create C2
        self.C2 = ChanceNode('RSV hospitalizition', (parameters.hospdaycost*parameters.hoptime+parameters.prob_ICU*parameters.icutime*parameters.ICU+parameters.sadcost+parameters.fadcost), parameters.hosputility, [self.C3, self.T3], [(1-parameters.Hos_MORTALITY_PROB), parameters.Hos_MORTALITY_PROB])
        # create C1
        self.C1 = ChanceNode('Palivizumab',parameters.cost_P_unit*parameters.weight, 0, [self.C2, self.C4], [parameters.probphops,(1-parameters.probphops)])
        # create C3
        self.C6 = ChanceNode('RSV hospitalizition', (parameters.hospdaycost*parameters.hoptime+parameters.prob_ICU*parameters.icutime*parameters.ICU+parameters.sadcost+parameters.fadcost), parameters.hosputility, [self.C7, self.T8], [(1-parameters.Hos_MORTALITY_PROB), parameters.Hos_MORTALITY_PROB])

        # create C1
        self.C8 = ChanceNode('No hospitalizition', 0, parameters.rsv_nh_u, [self.C2, self.T3], [(1-parameters.probnhpd),parameters.probnhpd])
        # create C1
        self.C5 = ChanceNode('No prophylaxis', 0, 0, [self.C6, self.C8], [parameters.hos_rate, (1-parameters.hos_rate)])
        # create C3



        # create D1
        self.D1 = DecisionNode('D1', 0, 0, [self.C1, self.C5])



params = P.Parameters()

mytree=tree(id=0, parameters=params)

mytree.C1.get_expected_utility()

print(mytree.C1.get_expected_utility())
print(mytree.C1.get_expected_cost())

print(mytree.C5.get_expected_utility())
print(mytree.C5.get_expected_cost())