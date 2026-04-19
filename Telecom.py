import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("dark")
plt.rcParams['figure.facecolor'] = '#121212'
plt.rcParams['axes.facecolor'] = '#121212'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['axes.titlecolor'] = 'white'
plt.rcParams['figure.edgecolor'] = 'white'


df = pd.read_csv("C:/Users/tanma/OneDrive/Desktop/5-Day python bootcamp/Comprehensive/Table_3.1.csv")

print("\nDataset Loaded Successfully")
print(df.head())

# Remove All India / Total rows
df = df[~df["State/overall"].str.contains("All India|Total|Service Area wise Subscribers - Overall", case=False, na=False)]

# Convert Year to int
df["At the end of March"] = df["At the end of March"].astype(int)

#Latest Year Data
latest_year = df["At the end of March"].max()
latest_df = df[df["At the end of March"] == latest_year]

print(f"\nLatest Year in Dataset: {latest_year}")

# 4. Top 10 States by Subscribers
top_states = (
    latest_df.groupby("State/overall")["Total"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 5))
top_states.plot(kind="bar", color='#FF9500')
plt.title("Top 10 States by Telecom Subscribers")
plt.xlabel("State")
plt.ylabel("Subscribers (in millions)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 5. Fastest Growing States

growth = df.groupby("State/overall").apply(
    lambda x: x.sort_values("At the end of March")["Total"].iloc[-1] -
              x.sort_values("At the end of March")["Total"].iloc[0]
)

fastest_growing = growth.sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 5))
fastest_growing.plot(kind="bar", color='#FF9500')
plt.title("Top 10 Fastest Growing States")
plt.xlabel("State")
plt.ylabel("Subscriber Growth (in millions)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 6. Rural vs Urban Analysis

ru_df = latest_df.groupby("State/overall")[["Rural", "Urban"]].sum()

ru_df["Rural %"] = (
    ru_df["Rural"] /
    (ru_df["Rural"] + ru_df["Urban"])
) * 100

ru_df["Urban %"] = 100 - ru_df["Rural %"]

# Rural-heavy States
rural_heavy = ru_df.sort_values("Rural %", ascending=False).head(10)

plt.figure(figsize=(10, 5))
plt.bar(rural_heavy.index, rural_heavy["Rural %"], color='#FF9500')
plt.title("Top 10 Rural-heavy States")
plt.ylabel("Rural Subscriber Percentage")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Urban-heavy States
urban_heavy = ru_df.sort_values("Urban %", ascending=False).head(10)

plt.figure(figsize=(10, 5))
plt.bar(urban_heavy.index, urban_heavy["Urban %"], color='#FF9500')
plt.title("Top 10 Urban-heavy States")
plt.ylabel("Urban Subscriber Percentage")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 7. Heatmap: State vs Year

pivot = df.pivot_table(
    values="Total",
    index="State/overall",
    columns="At the end of March",
    aggfunc="sum"
)

plt.figure(figsize=(12, 8))
sns.heatmap(pivot, cmap="plasma")
plt.title("State-wise Telecom Subscribers Heatmap")
plt.tight_layout()
plt.show()

print("\nAnalysis Completed Successfully")
