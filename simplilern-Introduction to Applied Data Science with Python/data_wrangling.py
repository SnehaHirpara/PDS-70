import pandas as pd
import numpy as np

data = {
    "name": ["A", "B", "C", "D", "E", "E"],
    "age": [20, 21, np.nan, 22, 20, 20],
    "marks": [80, 75, 90, np.nan, 85, 85],
    "city": ["Ahmedabad", "Surat", "Ahmedabad", "Vadodara", "Surat", "Surat"]
}

df = pd.DataFrame(data)

print(df)

print(df.isnull())

print(df.isnull().sum())

df["age"] = df["age"].fillna(df["age"].mean())

df["marks"] = df["marks"].fillna(df["marks"].mean())

print(df)

df = df.drop_duplicates()

print(df)

print(df[df["marks"] > 75])

print(df[(df["marks"] > 70) & (df["age"] > 20)])

df["marks"] = df["marks"] + 5

print(df)

df["passed"] = df["marks"] >= 40

print(df)

df = df.sort_values("marks", ascending=False)

print(df)

df = df.reset_index(drop=True)

print(df)

df["name"] = df["name"].str.lower()

print(df)

df["city"] = df["city"].str.upper()

print(df)

df["age"] = df["age"].astype(int)

print(df)

a = df[["name", "marks"]]

print(a)

b = df[["name", "city"]]

print(b)

c = pd.concat([a, b], axis=1)

print(c)

data2 = {
    "name": ["F", "G"],
    "age": [21, 23],
    "marks": [72, 88],
    "city": ["Rajkot", "Surat"]
}

df2 = pd.DataFrame(data2)

df = pd.concat([df, df2], ignore_index=True)

print(df)

print(df.groupby("city")["marks"].mean())

print(df.groupby("city")["marks"].sum())

print(df["marks"].max())
print(df["marks"].min())

q1 = df["marks"].quantile(0.25)
q3 = df["marks"].quantile(0.75)

iqr = q3 - q1

print(q1)
print(q3)
print(iqr)

lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

print(df[(df["marks"] < lower) | (df["marks"] > upper)])

df["marks_normal"] = (df["marks"] - df["marks"].min()) / (df["marks"].max() - df["marks"].min())

print(df)
