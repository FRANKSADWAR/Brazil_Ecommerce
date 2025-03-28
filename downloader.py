import requests
from pathlib import Path
from sentiment_analysis import re_special_characters

def download_one_file_of_raw_data(year: int, month: int) -> Path:
    URL = f"https://d37ci6vzurychx.cloudfromt.net/trip-data/yellow_trip_data-{year}-{month:02d}.parquet"
    response = requests.get(URL)

    if response.status_code == 200:
        path = f'.../data/raw_rides_{year}-{month:02d}.parquet'
        open(path, "wb").write(response.content)
        return path
    else:
        raise Exception(f'{URL} is not available')