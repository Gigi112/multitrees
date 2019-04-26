import numpy as np

Hos_MORTALITY_PROB = 0.0372
# annual probability of mortality
DRUG_EFFECT_RATIO = 0.75    # drug effectiveness:
                            # ratio of the annual mortality probability when using the drug to when not using the drug.
ALPHA = 0.05        # significance level

life_exp = 76

death_rate = 1/life_exp

DISCOUNT = 0.035

hos_rate = 0.097

reduce_risk = 0.453

cost_P_unit = 5.64

weight = 6.649

per_kid_cost = weight*15*cost_P_unit

length_hos = 12.40

cost_hos = 555

seq = 14015

prob_seq = 0.155

Asthma_utility = 0.952


# settings for simulation
POP_SIZE = 10000      # population size of the simulated cohort

hospital_utility = 0.88
rsv_nh_u =0.95    # No hospital
died_u = 0 # DEATH
survive_u = 0

initial_nurse = 41
seq_nurse = 31
ICU = 2225
prob_ICU = 0.3814


mu, sigma = 0.015, 0.068  # mean and standard deviation

s = np.random.normal(mu, sigma, 1000)

weight = 6649

hoptime = 12.4

icutime = 15.19

fadcost=41

sadcost=31