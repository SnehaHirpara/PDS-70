import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(a)
print(b)

print(a + b)
print(a - b)
print(a * b)

print(np.dot(a, b))

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

print(a)
print(b)

print(a + b)
print(a - b)

print(a * b)
print(np.dot(a, b))

print(a.T)

print(np.linalg.det(a))

print(np.linalg.inv(a))

print(np.linalg.matrix_rank(a))

a = np.array([[1, 2], [3, 4]])
b = np.array([5, 6])

print(np.linalg.solve(a, b))

x = np.array([1, 2, 3])
y = np.array([4, 5, 6])

print(np.linalg.norm(x))
print(np.linalg.norm(y))

print(np.cross(x, y))

a = np.array([[2, 1], [1, 3]])

eigenvalues, eigenvectors = np.linalg.eig(a)

print(eigenvalues)
print(eigenvectors)
