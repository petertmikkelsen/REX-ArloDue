import math
import numpy as np
import time

def norm(x, mu, sigma):
    return (1/(np.sqrt(2*np.pi)*sigma))*np.exp((-1/2)*(((x-mu)**2)/sigma**2))

def weight(x):
    return 0.3*norm(x, 2, 1)+0.4*norm(x, 5, 2) + 0.3*norm(x, 9, 1)

for i in range(15):
    #print(str(i+1) + ": " + str(weight(i+1)))
    pass

def uniform(k):
    list = []
    for i in range(k):
        list.append(math.floor(np.random.uniform(0, 16)))
    return list

def resample(samples):

    weights = np.zeros(len(samples))

    sum = 0
    for i in range(len(samples)):
        weights[i] = weight(samples[i])
        sum+=weights[i]
    weights = weights/np.sum(weights)

    resamples = np.zeros(len(samples))

    for i in range(len(samples)):
        resamples[i] = np.random.choice(samples, p=weights)

    return resamples


#resample(uniform(1000))
before = time.time()
resample(np.random.normal(5, 4, 1000))
after = time.time()
print(after-before)
