import pandas as pd
from os import getcwd, path

url: str = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

df: pd.DataFrame = pd.read_csv(url)

df.to_csv(path.join(getcwd(), "seeds/owid-covid-data.csv"), index=False)
print("Data saved successfully in the path: seeds/owid_covid.csv")