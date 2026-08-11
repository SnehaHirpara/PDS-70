import numpy as np
import statistics
import math

a = [10, 20, 30, 40, 50]

print(statistics.mean(a))
print(statistics.median(a))
print(statistics.mode(a))

print(statistics.variance(a))
print(statistics.stdev(a))

print(np.mean(a))
print(np.median(a))
print(np.var(a))
print(np.std(a))

b = [10, 10, 20, 30, 40]

print(statistics.mode(b))
print(statistics.median(b))

x = [2, 4, 6, 8, 10]

print(sum(x))
print(sum(x)/len(x))

p = 0.5

print(p)
print(1-p)

print(0.2 + 0.3)
print(0.5 * 0.4)

n = 10
r = 3

print(math.factorial(n))
print(math.comb(n, r))

p = 0.5

prob = math.comb(n, r) * (p ** r) * ((1-p) ** (n-r))

print(prob)

x = np.random.binomial(10, 0.5, 10)
print(x)

x = np.random.poisson(5, 10)
print(x)

x = np.random.normal(50, 10, 10)
print(x)

print(np.mean(x))
print(np.std(x))

data = np.array([12, 15, 18, 20, 25, 30, 35, 40])

print(np.percentile(data, 25))
print(np.percentile(data, 50))
print(np.percentile(data, 75))

print(np.corrcoef([1, 2, 3, 4, 5], [2, 4, 6, 8, 
