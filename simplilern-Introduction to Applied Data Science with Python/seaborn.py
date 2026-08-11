import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

data = {
    "name": ["A", "B", "C", "D", "E", "F"],
    "marks": [80, 65, 90, 70, 85, 75],
    "age": [20, 21, 19, 22, 20, 21]
}

df = pd.DataFrame(data)

print(df)

sns.lineplot(x="name", y="marks", data=df)
plt.show()

sns.barplot(x="name", y="marks", data=df)
plt.show()

sns.scatterplot(x="age", y="marks", data=df)
plt.show()

sns.histplot(df["marks"])
plt.show()

sns.boxplot(x=df["marks"])
plt.show()

sns.violinplot(x=df["marks"])
plt.show()

sns.countplot(x="age", data=df)
plt.show()

sns.pairplot(df)
plt.show()

print(df.corr(numeric_only=True))

sns.heatmap(df.corr(numeric_only=True), annot=True)
plt.show()

sns.set_style("darkgrid")

sns.barplot(x="name", y="marks", data=df, color="blue")
plt.title("Student Marks")
plt.show()
