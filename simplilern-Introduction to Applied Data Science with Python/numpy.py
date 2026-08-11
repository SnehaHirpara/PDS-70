import numpy as np

a = np.array([10, 20, 30, 40, 50])
print(a)
print(type(a))

print(a[0])
print(a[2])
print(a[-1])

print(a[1:4])

print(a.shape)
print(a.size)
print(a.ndim)
print(a.dtype)

b = np.array([1, 2, 3, 4, 5])

print(a + b)
print(a - b)
print(a * b)
print(a / b)

print(a + 10)
print(a * 2)

print(np.sum(a))
print(np.mean(a))
print(np.max(a))
print(np.min(a))
print(np.std(a))

a = np.array([[1, 2, 3], [4, 5, 6]])

print(a)
print(a.shape)
print(a.ndim)

print(a[0])
print(a[1])
print(a[0][1])
print(a[1][2])

print(a[:, 0])
print(a[:, 1])
print(a[0, :])

b = np.zeros(5)
print(b)

c = np.ones(5)
print(c)

d = np.arange(1, 11)
print(d)

e = np.arange(0, 10, 2)
print(e)

f = np.linspace(0, 10, 5)
print(f)

a = np.array([1, 2, 3, 4, 5, 6])

b = a.reshape(2, 3)

print(b)

print(b.shape)

a = np.array([[1, 2], [3, 4]])

print(a.T)

print(np.sum(a))
print(np.sum(a, axis=0))
print(np.sum(a, axis=1))

a = np.array([1, 2, 3, 4, 5])

print(np.sqrt(a))
print(np.square(a))
print(np.log(a))

a = np.array([10, 20, 30, 40, 50])

print(np.where(a > 25))
print(a[a > 25])

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(np.concatenate((a, b)))

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

print(np.concatenate((a, b)))
print(np.vstack((a, b)))
print(np.hstack((a, b)))

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

print(a + b)
print(a * b)

print(np.dot(a, b))

print(np.random.rand(5))
print(np.random.randint(1, 10, 5))
