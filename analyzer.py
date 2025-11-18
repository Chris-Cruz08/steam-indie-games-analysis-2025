import pandas as pd


def clean_and_enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    # Basic cleaning
    df = df.copy()
    df["price"] = pd.to_numeric(df["price"], errors="coerce") / 100  # price is in cents
    df["positive"] = pd.to_numeric(df["positive"], errors="coerce")
    df["negative"] = pd.to_numeric(df["negative"], errors="coerce")
    df["average_playtime"] = pd.to_numeric(df["average_forever"], errors="coerce")
    df["owners_avg"] = df["owners"].apply(lambda x: (int(x.split(" .. ")[0].replace(",", "")) +
                                                     int(x.split(" .. ")[1].replace(",", ""))) / 2)

    # Positive review ratio
    df["positive_ratio"] = df["positive"] / (df["positive"] + df["negative"]).replace(0, 1)

    # Playtime per dollar (minutes per $1) - avoid division by zero or free games
    df["playtime_per_dollar"] = df.apply(
        lambda row: row["average_playtime"] / row["price"] if row["price"] > 0 else 0, axis=1
    )

    # Very simple indie detection (SteamSpy has no perfect flag, so we use developer + owners)
    big_publishers = {"Valve", "Activision", "Electronic Arts", "Ubisoft", "Bethesda", "Square Enix",
                      "Warner Bros", "SEGA", "Capcom", "Rockstar", "2K", "Microsoft", "Sony", "Nintendo"}
    df["is_indie"] = df.apply(
        lambda row["developer"] not in big_publishers and row["publisher"] not in big_publishers
                              and row["owners_avg"] < 5_000_000, axis=1
    )

    return df