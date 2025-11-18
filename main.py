from data_fetcher import fetch_top_games
from analyzer import clean_and_enrich_data
from visualizer import plot_top20_indie_value, plot_scatter_price_vs_playtime, plot_comparison_box

if __name__ == "__main__":
    print("Downloading data from SteamSpy...")
    df_raw = fetch_top_games(pages=2)  # top 2000 games

    print("Cleaning and analyzing...")
    df = clean_and_enrich_data(df_raw)

    print("Generating charts...")
    plot_top20_indie_value(df)
    plot_scatter_price_vs_playtime(df)
    plot_comparison_box(df)

    # Show top 10 best value indie games in console too
    indie = df[df["is_indie"] & (df["price"] > 0)]
    top10 = indie.nlargest(10, "playtime_per_dollar")[["name", "price", "average_playtime", "playtime_per_dollar", "positive_ratio"]]
    print("\nTop 10 Best-Value Indie Games:")
    print(top10.to_string(index=False))

    print("\nDone! Check the /output folder for charts.")