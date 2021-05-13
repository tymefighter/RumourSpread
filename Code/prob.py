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

    def compute_acceptance_prob(self, degree, max_nbr_degree):
        
        return math.pow(degree, self.confidence_factor) \
            / math.pow(max_nbr_degree, self.confidence_factor)
