import numpy as np
from sklearn.neighbors import KernelDensity
from scipy.stats.distributions import norm
from sklearn.cluster import AffinityPropagation, MeanShift, estimate_bandwidth
from sklearn import metrics

from shapely.geometry import Polygon

def mode(x):

    x = np.array(x)
    
    # fit kde
    kde_skl = KernelDensity()
    kde_skl.fit(x[:, np.newaxis])

    # find max on log grid
    log_min = np.log(min(x)) / np.log(10)
    log_max = np.log(max(x)) / np.log(10)
    x_grid = np.logspace(log_min, log_max, 100000)
    log_pdf = kde_skl.score_samples(x_grid[:, np.newaxis])
    return x_grid[log_pdf.argmax()]

def median(x):
    return np.median(x)

def clusters(x):

    upper_left = []
    for i in x:
        print np.concatenate(i[0], i[1])
        upper_left.append(i[0] + i[1])

    x = np.array(upper_left)
    
    bandwidth = estimate_bandwidth(x, quantile=0.2, n_samples=100)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(x)
    print ms.labels_
    print ms.cluster_centers_

def cluster(x):
    fresh = {}
    for this_index, points in enumerate(x):
        this = Polygon(points)
        found = False
        for that_index, that in fresh.items():
            union = this.union(that)
            inter = this.intersection(that)
            overlap = inter.area / union.area
            if overlap > 0.5:
                if this.area >= that.area:
                    fresh[this_index] = this
                    if that_index in fresh:
                        del fresh[that_index]
                else:
                    fresh[that_index] = that
                    if this_index in fresh:
                        del fresh[this_index]
                found = True
                break
        if not found:
            fresh[this_index] = this

    result = []
    for i in fresh:
        result.append(x[i])
        # result.append(list(i.exterior.coords)[:-1])
    
    return result

if __name__ == '__main__':
    x = np.concatenate([norm(1000, 1.).rvs(400), norm(20000, 1.).rvs(100)])
    print x
    print mode(x)


    af = AffinityPropagation(preference=-50)
    af.fit(x[:, np.newaxis])
    print dir(af)
    print af.cluster_centers_indices_
    print len(af.cluster_centers_indices_)
