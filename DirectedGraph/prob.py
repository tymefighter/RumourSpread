import math

class Prob:

    def __init__(
        self, num_bits, 
        conservation_factor, confidence_factor
    ):
        self.max_entropy = num_bits
        self.conservation_factor = conservation_factor
        self.confidence_factor = confidence_factor

    def compute_distortion_prob(self, entropy):
        
        entropy_diff_frac = (self.max_entropy - entropy) / self.max_entropy
        return 1.0 \
            / (math.exp(entropy_diff_frac * self.conservation_factor) + 1)

    def compute_acceptance_prob(self, degree, max_nbr_outdegree, min_nbr_outdegree):

        max_outdeg_pow = math.pow(max_nbr_outdegree, self.confidence_factor) \
            if self.confidence_factor > 0 \
            else math.pow(min_nbr_outdegree, self.confidence_factor)
        
        return math.pow(degree, self.confidence_factor) \
            / max_outdeg_pow
