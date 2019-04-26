import MultiCohortClasses as Cls
import MultiCohortSupport as Support

N_Trees = 1000  # number of patients

# create a multi-cohort to simulate under no therapy
multi_Trees = Cls.MultiTrees(
    ids=range(N_Trees))

Support.print_outcomes(multi_Trees_outcome=multi_Trees.multiTreesOutcomes)


# print comparative outcomes
Support.print_comparative_outcomes(multi_trees_P=multi_Trees.multiTreesOutcomes,
                                   multi_trees_N=multi_Trees.multiTreesOutcomes)

# report the CEA results
Support.report_CEA_CBA(multi_trees_P=multi_Trees.multiTreesOutcomes,
                       multi_trees_N=multi_Trees.multiTreesOutcomes)