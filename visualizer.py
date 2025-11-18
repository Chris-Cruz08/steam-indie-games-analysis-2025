import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("darkgrid")
os.makedirs("output", exist_ok=True)


def plot_top20_indie_value(df):
    indie = df[df["is_indie"] & (df["price"] > 0) & (df["average_playtime"] > 60)].copy()
    top20 = indie.nlargest(20, "playtime_per_dollar")

    plt.figure(figsize=(12, 8))
    bars = plt.barh(range(len(top20)-1, -1, -1),
                    top20["playtime_per_dollar"],
                    color="#00bfff")
    plt.yticks(range(len(top20)), [f"{name} ({year})" for name, year in zip(top20["name"], top20["release_date"].str[:4])])
    plt.xlabel("Average Playtime (minutes) per $1 Spent")
    plt.title("Top 20 Best-Value Indie Games on Steam (2025 Data)\n(Higher = More Bang for Your Buck)")
    plt.tight_layout()
    plt.savefig("output/top20_indie_value.png", dpi=200)
    plt.close()


def plot_scatter_price_vs_playtime(df):
    sample = df.sample(n=800, random_state=42)  # for readability
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=sample, x="price", y="average_playtime",
                    hue="is_indie", palette={True: "#ff6b6b", False: "#4ecdc4"},
                    alpha=0.7, size="positive_ratio", sizes=(20, 200))
    plt.title("Price vs Average Playtime - Indie (red) vs AAA (teal)\nDot size = Positive Review Ratio")
    plt.xlabel("Price (USD)")
    plt.ylabel("Average Forever Playtime (minutes)")
    plt.xlim(0, 80)
    plt.ylim(0, df["average_playtime"].quantile(0.99))
    plt.legend(title="Indie Game")
    plt.tight_layout()
    plt.savefig("output/price_vs_playtime_scatter.png", dpi=200)
    plt.close()


def plot_comparison_box(df):
    comparison = df.melt(value_vars=["price", "average_playtime", "positive_ratio"],
                         id_vars=["is_indie"],
                         var_name="metric")
    comparison = comparison[comparison["is_indie"].isin([True, False])]

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=comparison, x="metric", y="value", hue="is_indie",
                palette={True: "#ff6b6b", False: "#4ecdc4"})
    plt.title("Indie vs AAA Games - Key Metrics Comparison")
    plt.xticks([0, 1, 2], ["Price (USD)", "Avg Playtime (min)", "Positive Review Ratio"])
    plt.legend(title="Indie Game")
    plt.tight_layout()
    plt.savefig("output/indie_vs_aaa_comparison.png", dpi=200)
    plt.close()