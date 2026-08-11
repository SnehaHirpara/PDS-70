import pandas as pd
import numpy as np

data = {
    "name": ["A", "B", "C", "D", "E", "F"],
    "age": [20, 21, 19, 22, 20, 21],
    "marks": [80, 75, 90, 65, 85, 70],
    "city": ["Ahmedabad", "Surat", "Ahmedabad", "Vadodara", "Surat", "Ahmedabad"]
}

df = pd.DataFrame(data)

print(df)

print(df.head())
print(df.shape)
print(df.info())
print(df.describe())

print(df["marks"].mean())
print(df["marks"].median())
print(df["marks"].max())
print(df["marks"].min())

print(df["age"].value_counts())
print(df["city"].value_counts())

print(df.groupby("city")["marks"].mean())

print(df.groupby("age")["marks"].mean())

print(df[df["marks"] > 75])

print(df[(df["marks"] > 70) & (df["age"] >= 20)])

print(df.sort_values("marks", ascending=False))

print(df.corr(numeric_only=True))

print(df["marks"].std())
print(df["marks"].var())

print(df["marks"].describe())

a = df["marks"]

print(np.mean(a))
print(np.median(a))
print(np.std(a))

print(df["marks"].quantile(0.25))
print(df["marks"].quantile(0.50))
print(df["marks"].quantile(0.75))

df["result"] = np.where(df["marks"] >= 40, "Pass", "Fail")

print(df)

print(df.groupby("result").size())

print(df.groupby("city")["marks"].agg(["mean", "max", "min"]))

print(df.nlargest(3, "marks"))

print(df.nsmallest(3, "marks"))
