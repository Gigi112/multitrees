from DecisionTree import tree
from Parameterclass import ParameterGenerator
import SimPy.RandomVariantGenerators as RVGs
import SimPy.StatisticalClasses as Stat


class MultiTrees:
    """ simulates multiple cohorts with different parameters """

    def __init__(self, ids):
        """
        :param ids: (list) of ids for cohorts to simulate
        :param pop_size: (int) population size of cohorts to simulate
        :param therapy: selected therapy
        """
        self.ids = ids
        self.param_sets = []  # list of parameter sets each of which corresponds to a cohort
        self.trees = []
        self.multiTreesOutcomes = MultiTreesOutcomes()

        # create parameter sets
        self.__populate_parameter_sets()

        # create cohorts
        for i in range(len(self.ids)):
            self.trees.append(tree(id=self.ids[i],
                                   parameters=self.param_sets[i]))

    def __populate_parameter_sets(self):

        # create a parameter set generator
        param_generator = ParameterGenerator()

        # create as many sets of parameters as the number of cohorts
        for i in range(len(self.ids)):
            # create a new random number generator for each parameter set
            rng = RVGs.RNG(seed=i)
            # get and store a new set of parameter
            self.param_sets.append(param_generator.get_new_parameters(rng=rng))

    def simulate(self):
        """ simulates all cohorts
        :param sim_length: simulation length
        """

        for tree in self.trees:

            # extract the outcomes of this simulated cohort
            self.multiTreesOutcomes.extract_outcomes(simulated_tree=tree)


        # clear cohorts (to free up the memory that was allocated to these cohorts)
        self.trees.clear()


class MultiTreesOutcomes:

    def __init__(self):
        self.PCosts = []         # patient cost from each simulated tree
        self.PQALYs = []         # patient QALY from each simulated tree

        self.NCosts = []  # list of patient cost from each simulated tree
        self.NQALYs = []  # list of patient QALY from each simulated tree

        self.statMeanPCost = None  # summary statistics of average cost
        self.statMeanPQALY = None

        self.statMeanNCost = None  # summary statistics of average cost
        self.statMeanNQALY = None

    def extract_outcomes(self, simulated_tree):
        """ extracts outcomes of a simulated cohort
        :param simulated_cohort: a cohort after being simulated"""

        # store mean cost from this patient
        self.PCosts.append(simulated_tree.C1.get_expected_cost())
        self.PQALYs.append(simulated_tree.C1.get_expected_utility())
        # store mean QALY from this patient
        self.NCosts.append(simulated_tree.C5.get_expected_cost())
        self.NQALYs.append(simulated_tree.C5.get_expected_utility())

    def calculate_summary_stats(self):
        """
        calculate the summary statistics
        """
        # summary statistics of mean cost
        self.statMeanPCost = Stat.SummaryStat(name='Average Palivizumab cost',
                                             data=self.PCosts)
        # summary statistics of mean QALY
        self.statMeanPQALY = Stat.SummaryStat(name='Average Palivizumab QALY',
                                             data=self.PQALYs)

        self.statMeanNCost = Stat.SummaryStat(name='Average no prophylaxis cost',
                                              data=self.NCosts)
        # summary statistics of mean QALY
        self.statMeanNQALY = Stat.SummaryStat(name='Average no prophylaxis QALY',
                                              data=self.NQALYs)

