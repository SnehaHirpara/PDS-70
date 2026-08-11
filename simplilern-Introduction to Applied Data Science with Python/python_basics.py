a = 10
b = 20

print(a)
print(b)
print(a+b)

x = 10.5
name = "python"
flag = True

print(type(x))
print(type(name))
print(type(flag))

print(10+5)
print(10-5)
print(10*5)
print(10/5)
print(10//3)
print(10%3)
print(2**3)

a = 10
b = 20

print(a > b)
print(a < b)
print(a == b)
print(a != b)

print(a < 20 and b > 10)
print(a > 20 or b > 10)

name = input("Enter name: ")
age = int(input("Enter age: "))

print(name)
print(age)

if age >= 18:
    print("Adult")
else:
    print("Not adult")

a = [10, 20, 30, 40, 50]

print(a)
print(a[0])
print(a[-1])

a.append(60)
print(a)

a.remove(30)
print(a)

t = (10, 20, 30, 40)
print(t)
print(t[1])

s = {10, 20, 30, 20, 10}
print(s)

s.add(40)
print(s)

student = {
    "name": "Vasu",
    "age": 20,
    "marks": 85
}

print(student)
print(student["name"])
print(student["marks"])

text = "Python for Data Science"

print(text)
print(len(text))
print(text.upper())
print(text.lower())
print(text[0:6])

for i in range(5):
    print(i)

i = 1

while i <= 5:
    print(i)
    i = i + 1

for i in range(10):
    if i == 5:
        break
    print(i)

for i in range(10):
    if i == 5:
        continue
    print(i)

def add(a, b):
    return a + b

print(add(10, 20))

import math

print(math.sqrt(25))
print(math.pi)

import random

print(random.randint(1, 10))
