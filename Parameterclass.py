import InputData as Data
import SimPy.RandomVariantGenerators as RVGs
import SimPy.FittingProbDist_MM as MM
import math
import scipy.stats as stat


class Parameters:

    def __init__(self):


        self.discountRate = Data.DISCOUNT
        self.dieutility = 0
        self.healthutility = 1
        self.palivizumabcosts = Data.cost_P_unit
        self.seqcost = 28030
        self.Hos_MORTALITY_PROB = 0.0372
        # annual probability of mortality
        DRUG_EFFECT_RATIO = 0.75  # drug effectiveness:
        # significance level
        self.life_exp = 76
        self.probnhpd = 1 / self.life_exp
        self.DISCOUNT = 0.035
        self.hos_rate = 0.097
        self.reduce_risk = 0.453
        self.probphops = self.hos_rate*(1-self.reduce_risk)
        self.cost_P_unit = 5.64
        self.weight = 6.649
        self.per_kid_cost = self.weight * 15 * self.cost_P_unit
        self.length_hos = 12.40
        self.hospdaycost = 555
        self.seq = 14015
        self.prob_seq = 0.155
        self.sequtility = 0.952
        # settings for simulation
        self.POP_SIZE = 10000  # population size of the simulated cohort
        self.hosputility = 0.88
        self.rsv_nh_u = 0.95  # No hospital
        self.initial_nurse = 41
        self.seq_nurse = 31
        self.ICU = 2225
        self.prob_ICU = 0.3814
        self.weight = 6649
        self.hoptime = 12.4
        self.icutime = 15.19
        self.fadcost=0
        self.sadcost=0
        # add all the parameters here, initial value doesn't matter



class ParameterGenerator:

    def __init__(self):

        self.hospdaycost = None
        self.fadcost = None
        self.sadcost = None
        self.icucost = None


        self.sequtility = None # annual state utilities
        self.hosputility = None
        self.rsvinfection = None   # list of dirichlet distributions for transition probabilities
        self.lnRelativeRiskRVG = None
        self.probnhpd = None
        # normal distribution for the natural log of the treatment relative risk


        self.probhops = None
        self.probICU = None
        self.probhpd = None
        self.probseq = None

        self.weight = None
        self.hoptime = None
        self.icutime = None

        # hospital cost
        # per unit P cost


        # utility
        hua = MM.get_beta_params(mean=Data.hospital_utility, st_dev=0.07)

        self.hosputility = RVGs.Beta(a=hua["a"], b=hua["b"])

        nhu = MM.get_beta_params(mean=Data.rsv_nh_u, st_dev=0.07)
        # append the distribution
        self.rsvinfection = RVGs.Beta(a=nhu["a"], b=nhu["b"])

        seq = MM.get_beta_params(mean=Data.Asthma_utility, st_dev=0.07)
        # append the distribution
        self.sequtility = RVGs.Beta(a=seq["a"], b=seq["b"])


        ##### cost

        hos = MM.get_gamma_params(mean=Data.cost_hos, st_dev=149)
        # append the distribution
        self.hospdaycost = RVGs.Gamma(a=hos["a"],
                               loc=0,
                               scale=hos["scale"])

        icu = MM.get_gamma_params(mean=Data.ICU, st_dev=271)
        # append the distribution
        self.icucost = RVGs.Gamma(a=icu["a"],
                               loc=0,
                               scale=icu["scale"])

        sad = MM.get_gamma_params(mean=Data.sadcost, st_dev=5)
        # append the distribution
        self.sadcost = RVGs.Gamma(a=sad["a"],
                                  loc=0,
                                  scale=icu["scale"])
        fad = MM.get_gamma_params(mean=Data.fadcost, st_dev=6)
        # append the distribution
        self.fadcost = RVGs.Gamma(a=fad["a"],
                                  loc=0,
                                  scale=icu["scale"])

        ##### prob

        hp = MM.get_beta_params(mean=Data.hos_rate, st_dev=0.023)
        # append the distribution
        self.probhops = RVGs.Beta(a=hp["a"], b=hp["b"])


        hu = MM.get_beta_params(mean=Data.prob_ICU, st_dev=0.0967)
        # append the distribution
        self.probICU = RVGs.Beta(a=hu["a"], b=hu["b"])

        dea = MM.get_beta_params(mean=Data.Hos_MORTALITY_PROB, st_dev=0.0253)
        # append the distribution
        self.probhpd = RVGs.Beta(a=dea["a"], b=dea["b"])

        se = MM.get_beta_params(mean=Data.prob_seq, st_dev=0.115)
        # append the distribution
        self.probseq = RVGs.Beta(a=se["a"], b=se["b"])

        de = MM.get_beta_params(mean=Data.death_rate, st_dev=0.0004836235)
        self.probnhpd = RVGs.Beta(a=de["a"], b=de["b"])


        ### stay time

        hoss = MM.get_gamma_params(mean=Data.hoptime, st_dev=3.1)
        # append the distribution
        self.hoptime = RVGs.Gamma(a=hoss["a"],
                                      loc=0,
                                      scale=hoss["scale"])

        ic = MM.get_gamma_params(mean=Data.icutime, st_dev=3.8)
        # append the distribution
        self.icutime = RVGs.Gamma(a=ic["a"],
                                  loc=0,
                                  scale=ic["scale"])

        ## weight

        we = MM.get_gamma_params(mean=Data.weight, st_dev=392)
        # append the distribution
        self.weight = RVGs.Gamma(a=we["a"],
                                      loc=0,
                                      scale=we["scale"])

        rr_ci = [0.181, 0.634]   # confidence interval of the treatment relative risk

        # find the mean and st_dev of the normal distribution assumed for ln(RR)
        # sample mean ln(RR)
        mean_ln_rr = math.log(0.453)
        # sample standard deviation of ln(RR)
        std_ln_rr = \
            (math.log(rr_ci[1]) - math.log(rr_ci[0])) / (2 * stat.norm.ppf(1 - 0.05 / 2))
        # create a normal distribution for ln(RR)
        self.lnRelativeRiskRVG = RVGs.Normal(loc=mean_ln_rr,
                                             scale=std_ln_rr)

    def get_new_parameters(self, rng):

        param = Parameters()

        param.hospdaycost = self.hospdaycost.sample(rng)
        param.fadcost = self.fadcost.sample(rng)
        param.sadcost = self.sadcost.sample(rng)
        param.ICU = self.icucost.sample(rng)

        param.sequtility = self.sequtility.sample(rng)  # annual state utilities
        param.hosputility = self.hosputility.sample(rng)
        param.rsvinfection = self.rsvinfection.sample(rng)
        param.lnRelativeRiskRVG = self.lnRelativeRiskRVG.sample(rng)
        param.rr = math.exp(self.lnRelativeRiskRVG.sample(rng))
        # calculate probabilities between treatment
        param.weight = self.weight.sample(rng)
        param.hoptime = self.hoptime.sample(rng)
        param.icutime = self.icutime.sample(rng)

        param.probnhpd = self.probnhpd.sample(rng)
        param.probICU = self.probICU.sample(rng)
        param.Hos_MORTALITY_PROB = self.probhpd.sample(rng)
        param.prob_seq = self.probseq.sample(rng)
        param.probnhps = 1-param.probnhpd

              # list of dirichlet distributions for transition probabilitie
        param.hos_rate = self.probhops.sample(rng)

        param.probphops = self.probhops.sample(rng)*param.rr

            # calculate transition probability matrix for the combination therapy

        return param



