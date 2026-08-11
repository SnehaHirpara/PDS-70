import pandas as pd

a = [10, 20, 30, 40, 50]

s = pd.Series(a)

print(s)
print(s[0])
print(s[2])

data = {
    "name": ["A", "B", "C", "D", "E"],
    "age": [20, 21, 19, 22, 20],
    "marks": [80, 75, 90, 65, 85]
}

df = pd.DataFrame(data)

print(df)
print(df.head())
print(df.tail())

print(df.shape)
print(df.columns)
print(df.dtypes)

print(df["name"])
print(df["marks"])

print(df[["name", "marks"]])

print(df.iloc[0])
print(df.iloc[1:4])

print(df.loc[0, "name"])
print(df.loc[2, "marks"])

print(df[df["marks"] > 80])

print(df[df["age"] >= 20])

print(df.sort_values("marks"))

print(df.sort_values("marks", ascending=False))

print(df["marks"].mean())
print(df["marks"].median())
print(df["marks"].max())
print(df["marks"].min())
print(df["marks"].sum())

print(df.describe())

df["passed"] = df["marks"] >= 40

print(df)

df["bonus"] = 5

print(df)

df["total"] = df["marks"] + df["bonus"]

print(df)

df = df.drop("bonus", axis=1)

print(df)

data2 = {
    "name": ["F", "G"],
    "age": [21, 20],
    "marks": [70, 95]
}

df2 = pd.DataFrame(data2)

df = pd.concat([df, df2], ignore_index=True)

print(df)

print(df.isnull())

print(df.isnull().sum())

df.loc[2, "marks"] = None

print(df)

df["marks"] = df["marks"].fillna(df["marks"].mean())

print(df)

df = df.drop_duplicates()

print(df)

print(df.groupby("age")["marks"].mean())

print(df["marks"].value_counts())
