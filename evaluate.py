#import math
import scipy.stats
import matplotlib.pyplot as plt
import operator

class Evaluation:
    """
    This class implements methods for evulating word representations.
    """

    def __init__(self):
        pass

    def rank_correlation(self, list1, list2):
        """
        Calculate the ranked correlation between items that are in commen between the two list of scores.
        """
        return scipy.stats.spearmanr(list1, list2)

    def asymmetry(self, scores, pairs):
        """
        Find the ratio of p(w1|w2)/p(w2|w1) for pairs that both probabilities exist (is a number)
        and at least one of the probabilities is greater than zero.
        """
        ratios = []
        differences = []
        for cue, target in pairs:
           # differences.append(math.fabs(scores[cue][target] - scores[target][cue]))
            differences.append(scores[cue][target] - scores[target][cue])

            try:
                #ratios.append(max(scores[cue][target], scores[target][cue]) \
                #        / min(scores[cue][target], scores[target][cue]))
                ratios.append(scores[cue][target]  / scores[target][cue])

            except ZeroDivisionError:
                ratios.append(float('inf'))
        return ratios, differences


    def _not_triangle_inequality(self, norms):
        """
        Find pairs for which the triangle inequality does not hold, that is, d(z,z) > d(x,y) + d(y,z).
        Shows that to what extent we can treat the similarities as a distance metric.
        """
        return


    def traingle_inequality_threshold(self, tuples, scores, thresholds):
        """
        Find the pairs such that P(w2|w1) and P(w3|w2) are greater than the threshold;
        plot the distribution of P(w3|w1).

        Traingle inequaliy: P(w2|w1) + P(w3|w2) >= P(w3|w1)

        This is based on Griffiths et al. (2007).

        scores: dictionary in the format of scores[w1][w2] = value
        differences holds P(w2|w1) + P(w3|w2) - P(w3|w1)

        """
        prob_dist_thresh = {}
        differences = []
        ratios = []
        for t in thresholds:
            prob_dist_thresh[t] = []

        for w1,w2,w3 in tuples:
            # TODO: this can be done more efficiently, not need to do this for all the thresholds
            for t in thresholds:
                if scores[w1][w2] >= t and scores[w2][w3] >= t:
                    prob_dist_thresh[t].append(scores[w1][w3])
            #print(t, len(prob_dist_thresh[t]))
            #
            differences.append(min(scores[w1][w2], scores[w2][w3]) - scores[w1][w3])
            ratios.append(min(scores[w1][w2], scores[w2][w3]) / scores[w1][w3])

            #print((w1,w2,w3), differences[-1])

        return prob_dist_thresh, differences, ratios


    def plot_traingle_inequality(self, dist, name):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #
        for thres in dist:
            print(name, thres, len(dist[thres]))
            ax.hist(dist[thres], label=str(thres))
        ax.set_ylim(0, 100)
        ax.legend()
        fig.savefig(name)

    def sort_scores(self, scores):
        sorted_scores = {}
        for cue in scores:
            sorted_scores[cue] = sorted(scores[cue].items(), key=operator.itemgetter(1))
        return sorted_scores


    def median_rank(self, gold, scores, n):
        """ calculate the median rank of the first n associates """
        ranks = {}
        for r in range(n):
            ranks[r] = []

        for cue in gold:
            for index in range(min(len(gold[cue]), n)):
                target = gold[cue][index][0]
                for j in range(len(scores[cue])):
                    if scores[cue][j][0] == target:
                        ranks[index].append(j+1)
        return ranks




