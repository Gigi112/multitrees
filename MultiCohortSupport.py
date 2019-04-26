import InputData as D
import SimPy.StatisticalClasses as Stat
import SimPy.EconEvalClasses as Econ
import matplotlib.pyplot as plt


def print_outcomes(multi_Trees_outcome):
    """ prints the outcomes of a simulated cohort
    :param multi_cohort_outcomes: outcomes of a simulated multi-cohort
    :param therapy_name: the name of the selected therapy
    """

    # mean and prediction interval text of discounted total cost
    Pcost_mean_PI_text = multi_Trees_outcome.MultiTreesOutcomes.statMeanPCost\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    # mean and prediction interval text of discounted total QALY
    Putility_mean_PI_text = multi_Trees_outcome.statMeanPQALY\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=2)

    Ncost_mean_PI_text = multi_Trees_outcome.statMeanNCost \
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    # mean and prediction interval text of discounted total QALY
    Nutility_mean_PI_text = multiTrees.statMeanNQALY \
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=2)


    # print outcomes
    print("  Estimate of mean discounted Palivizumab cost and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          Pcost_mean_PI_text)
    print("  Estimate of mean discounted Palivizumab utility and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          Putility_mean_PI_text)
    print("  Estimate of mean discounted no prophylaxis cost and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          Ncost_mean_PI_text)
    print("  Estimate of mean discounted no prophylaxis utility and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          Nutility_mean_PI_text)



def print_comparative_outcomes(multi_trees_P, multi_trees_N):
    """ prints average increase in discounted cost, and discounted utility
    under combination therapy compared to mono therapy
    :param multi_trees_P: outcomes of a multi-trees simulated under Palivizumab
    :param multi_trees_N: outcomes of a multi-trees simulated under no prophylaxis
    """

    # increase in mean discounted cost under combination therapy with respect to mono therapy
    increase_mean_discounted_cost = Stat.DifferenceStatPaired(
        name='Increase in mean discounted cost',
        x=multi_trees_P.PCosts,
        y_ref=multi_trees_N.NCosts)

    # estimate and PI
    estimate_PI = increase_mean_discounted_cost.get_formatted_mean_and_interval(interval_type='p',
                                                                                alpha=D.ALPHA,
                                                                                deci=2,
                                                                                form=',')
    print("Increase in mean discounted cost and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean discounted QALY under combination therapy with respect to mono therapy
    increase_mean_discounted_qaly = Stat.DifferenceStatPaired(
        name='Increase in mean discounted QALY',
        x=multi_trees_P.PQALYs,
        y_ref=multi_trees_N.NQALYs)

    # estimate and PI
    estimate_PI = increase_mean_discounted_qaly.get_formatted_mean_and_interval(interval_type='p',
                                                                                alpha=D.ALPHA,
                                                                                deci=2)
    print("Increase in mean discounted utility and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)


def report_CEA_CBA(multi_trees_P, multi_trees_N):
    """ performs cost-effectiveness and cost-benefit analyses
    :param multi_cohort_outcomes_mono: outcomes of a multi-cohort simulated under mono therapy
    :param multi_cohort_outcomes_combo: outcomes of a multi-cohort simulated under combination therapy
    """

    # define two strategies
    Palivizumab_therapy_strategy = Econ.Strategy(
        name='Palivizumab Therapy',
        cost_obs=multi_trees_P.PCosts,
        effect_obs=multi_trees_P.PQALYs,
        color='green'
    )
    No_prophylaxis_strategy = Econ.Strategy(
        name='No Prophylaxis',
        cost_obs=multi_trees_N.NCosts,
        effect_obs=multi_trees_N.NQALYs,
        color='blue'
    )

    # do CEA
    CEA = Econ.CEA(
        strategies=[Palivizumab_therapy_strategy, No_prophylaxis_strategy],
        if_paired=True
    )

    # show the cost-effectiveness plane
    show_ce_figure(CEA=CEA)

    # report the CE table
    CEA.build_CE_table(
        interval_type='p',  # prediction intervals
        alpha=D.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2)

    # CBA
    NBA = Econ.CBA(
        strategies=[Palivizumab_therapy_strategy, No_prophylaxis_strategy],
        if_paired=True
    )
    # show the net monetary benefit figure
    NBA.graph_incremental_NMBs(
        min_wtp=0,
        max_wtp=5000000,
        title='Cost-Benefit Analysis',
        x_label='Willingness-To-Pay for One Additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval_type='p',
        show_legend=True,
        figure_size=(6, 5)
    )


def show_ce_figure(CEA):

    # create a cost-effectiveness plot
    plt.figure(figsize=(5, 5))

    # find the frontier (x, y)'s
    frontier_utilities = []
    frontier_costs = []
    for s in CEA.get_shifted_strategies_on_frontier():
        frontier_utilities.append(s.aveEffect)
        frontier_costs.append(s.aveCost)

    # draw the frontier line
    plt.plot(frontier_utilities, frontier_costs,
             c='k',  # color
             alpha=0.6,  # transparency
             linewidth=2,  # line width
             label="Frontier")  # label to show in the legend

    # add the strategies
    for s in CEA.get_shifted_strategies():
        # add the center of the cloud
        plt.scatter(s.aveEffect, s.aveCost,
                    c=s.color,      # color
                    alpha=1,        # transparency
                    marker='o',     # markers
                    s=75,          # marker size
                    label=s.name    # name to show in the legend
                    )
        # add the cloud
        plt.scatter(s.effectObs, s.costObs,
                    c=s.color,  # color of dots
                    alpha=0.15,  # transparency of dots
                    s=25,  # size of dots
                    )

    plt.legend()        # show the legend
    plt.axhline(y=0, c='k', linewidth=0.5)  # horizontal line at y = 0
    plt.axvline(x=0, c='k', linewidth=0.5)  # vertical line at x = 0
    plt.xlim([-2, 8])              # x-axis range
    plt.ylim([-20000, 120000])     # y-axis range
    plt.title('Cost-Effectiveness Analysis')
    plt.xlabel('Additional discounted QALY')
    plt.ylabel('Additional discounted cost')
    plt.show()
