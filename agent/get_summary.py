

import pandas as pd
import numpy as np

def auto_summarize_dataframe(data: list, max_samples_per_metric: int = 10, max_countries: int = 20) -> str:
    df = pd.DataFrame(data)
    if df.empty:
        return "No data available."

    required_columns = {"location", "date", "iso_code", "population"}
    missing = required_columns - set(df.columns)

    if missing:
        return "Missing required columns. Cannot proceed."

    df = df[~df["iso_code"].str.startswith("OWID_")]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "population"])
    df = df[df["population"] > 0]

    metrics = [
        "new_cases", "new_deaths", "new_tests", "new_vaccinations", "total_cases", "total_deaths", "total_vaccinations"
    ]
    existing_cols = [col for col in metrics if col in df.columns]

    selected_countries = []
    grouped = df.groupby("location")

    for location, group in grouped:
        group = group.sort_values("date")
        if group.shape[0] < 10:
            continue

        population = group["population"].iloc[-1]

        for col in existing_cols:
            series = group[["date", col]].dropna()
            if series.empty:
                continue

            # Apenas para o filtro: normalizado por milhão
            per_million = (series[col] / population) * 1_000_000

            avg = per_million.mean()
            median = per_million.median()
            std = per_million.std()
            max_val = per_million.max()
            max_idx = per_million.idxmax()
            max_date = series.loc[max_idx, "date"]
            first_date = series["date"].min()
            total_days = (series["date"].max() - first_date).days + 1
            days_to_peak = (max_date - first_date).days + 1

            if (
                max_val > avg + 3 * std or
                max_val > 10 * median or
                max_val > 1000 or
                days_to_peak < 0.2 * total_days
            ):
                selected_countries.append((location, group, population))
                break

        if len(selected_countries) >= max_countries:
            break

    output = []
    for location, group, population in selected_countries:
        start_date = group["date"].min().strftime("%Y-%m-%d")
        end_date = group["date"].max().strftime("%Y-%m-%d")
        output.append(f"Location: {location}")
        output.append(f"Date Range: {start_date} to {end_date}")
        output.append(f"Population: {int(population):,}")

        for col in existing_cols:
            series = group[["date", col]].dropna()
            if series.empty:
                continue

            avg = series[col].mean().round(2)
            min_val = series[col].min().round(2)
            max_val = series[col].max().round(2)
            count = len(series)

            output.append(f"  Metric: {col}")
            output.append(f"    Count: {count}, Avg: {avg}, Min: {min_val}, Max: {max_val}")

            n_samples = min(50, count)
            sample_indices = np.linspace(0, count - 1, num=n_samples, dtype=int)
            sampled = series.iloc[sample_indices]
            
            for _, row in sampled.iterrows():
                date_str = row["date"].strftime("%Y-%m-%d")
                value = round(row[col], 2)
                output.append(f"    Sample: {date_str} -> {value}")

        output.append("")

    return "\n".join(output)