"""
Economic Indicators by U.S. President 
Stream Lit
"""

from pathlib import Path
import pickle
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from playwright.sync_api import sync_playwright



CACHE_DIR = Path("project_cache")
PROJECT_CACHE_FILE = CACHE_DIR / "project_cache.pkl"
CLEANED_CACHE_FILE = CACHE_DIR / "project_cache_cleaned.pkl"

URLS = {
    "unemployment": "https://www.macrotrends.net/datasets/1316/us-national-unemployment-rate",
    "inflation": "https://www.macrotrends.net/datasets/2497/historical-inflation-rate-by-year",
    "debt_to_gdp": "https://www.macrotrends.net/datasets/1381/debt-to-gdp-ratio-historical-chart",
    "housing_starts": "https://www.macrotrends.net/datasets/1314/housing-starts-historical-char",
}

INDIVIDUAL_CACHE_FILES = {
    "unemployment": CACHE_DIR / "unemployment.pkl",
    "inflation": CACHE_DIR / "inflation.pkl",
    "debt_to_gdp": CACHE_DIR / "debt_to_gdp.pkl",
    "housing_starts": CACHE_DIR / "housing_starts.pkl",
}


PRESIDENT_TERMS = [
    {"president": "George Washington", "party": "No Party", "start": 1789, "end": 1797},
    {"president": "John Adams", "party": "Federalist", "start": 1797, "end": 1801},
    {"president": "Thomas Jefferson", "party": "Democratic-Republican", "start": 1801, "end": 1809},
    {"president": "James Madison", "party": "Democratic-Republican", "start": 1809, "end": 1817},
    {"president": "James Monroe", "party": "Democratic-Republican", "start": 1817, "end": 1825},
    {"president": "John Quincy Adams", "party": "Democratic-Republican", "start": 1825, "end": 1829},
    {"president": "Andrew Jackson", "party": "Democrat", "start": 1829, "end": 1837},
    {"president": "Martin Van Buren", "party": "Democrat", "start": 1837, "end": 1841},
    {"president": "William Henry Harrison", "party": "Whig", "start": 1841, "end": 1841},
    {"president": "John Tyler", "party": "Whig", "start": 1841, "end": 1845},
    {"president": "James K. Polk", "party": "Democrat", "start": 1845, "end": 1849},
    {"president": "Zachary Taylor", "party": "Whig", "start": 1849, "end": 1850},
    {"president": "Millard Fillmore", "party": "Whig", "start": 1850, "end": 1853},
    {"president": "Franklin Pierce", "party": "Democrat", "start": 1853, "end": 1857},
    {"president": "James Buchanan", "party": "Democrat", "start": 1857, "end": 1861},
    {"president": "Abraham Lincoln", "party": "Republican", "start": 1861, "end": 1865},
    {"president": "Andrew Johnson", "party": "Democrat", "start": 1865, "end": 1869},
    {"president": "Ulysses S. Grant", "party": "Republican", "start": 1869, "end": 1877},
    {"president": "Rutherford B. Hayes", "party": "Republican", "start": 1877, "end": 1881},
    {"president": "James Garfield", "party": "Republican", "start": 1881, "end": 1881},
    {"president": "Chester Arthur", "party": "Republican", "start": 1881, "end": 1885},
    {"president": "Grover Cleveland", "party": "Democrat", "start": 1885, "end": 1889},
    {"president": "Benjamin Harrison", "party": "Republican", "start": 1889, "end": 1893},
    {"president": "Grover Cleveland", "party": "Democrat", "start": 1893, "end": 1897},
    {"president": "William McKinley", "party": "Republican", "start": 1897, "end": 1901},
    {"president": "Theodore Roosevelt", "party": "Republican", "start": 1901, "end": 1909},
    {"president": "William Howard Taft", "party": "Republican", "start": 1909, "end": 1913},
    {"president": "Woodrow Wilson", "party": "Democrat", "start": 1913, "end": 1921},
    {"president": "Warren Harding", "party": "Republican", "start": 1921, "end": 1923},
    {"president": "Calvin Coolidge", "party": "Republican", "start": 1923, "end": 1929},
    {"president": "Herbert Hoover", "party": "Republican", "start": 1929, "end": 1933},
    {"president": "Franklin D. Roosevelt", "party": "Democrat", "start": 1933, "end": 1945},
    {"president": "Harry Truman", "party": "Democrat", "start": 1945, "end": 1953},
    {"president": "Dwight Eisenhower", "party": "Republican", "start": 1953, "end": 1961},
    {"president": "John F. Kennedy", "party": "Democrat", "start": 1961, "end": 1963},
    {"president": "Lyndon Johnson", "party": "Democrat", "start": 1963, "end": 1969},
    {"president": "Richard Nixon", "party": "Republican", "start": 1969, "end": 1974},
    {"president": "Gerald Ford", "party": "Republican", "start": 1974, "end": 1977},
    {"president": "Jimmy Carter", "party": "Democrat", "start": 1977, "end": 1981},
    {"president": "Ronald Reagan", "party": "Republican", "start": 1981, "end": 1989},
    {"president": "George H. W. Bush", "party": "Republican", "start": 1989, "end": 1993},
    {"president": "Bill Clinton", "party": "Democrat", "start": 1993, "end": 2001},
    {"president": "George W. Bush", "party": "Republican", "start": 2001, "end": 2009},
    {"president": "Barack Obama", "party": "Democrat", "start": 2009, "end": 2017},
    {"president": "Donald Trump", "party": "Republican", "start": 2017, "end": 2021},
    {"president": "Joe Biden", "party": "Democrat", "start": 2021, "end": 2025},
    {"president": "Donald Trump", "party": "Republican", "start": 2025, "end": 2029},
]
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from pathlib import Path
import pandas as pd
import pickle
import streamlit as st

CACHE_DIR = Path("cache")
PROJECT_CACHE_FILE = CACHE_DIR / "project_cache.pkl"

# 

INDIVIDUAL_CACHE_FILES = {
    name: CACHE_DIR / f"{name}.pkl"
    for name in URLS
}


def scrape_table(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            page = browser.new_page(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )

            page.goto(url, wait_until="domcontentloaded", timeout=60000)

            try:
                page.wait_for_selector("table", timeout=15000)
            except PlaywrightTimeoutError:
                print(f"No table loaded on: {url}")
                browser.close()
                return pd.DataFrame()

            html = page.content()
            browser.close()

        tables = pd.read_html(html)

        if len(tables) == 0:
            return pd.DataFrame()

        return tables[0]

    except PlaywrightTimeoutError:
        print(f"Timeout while scraping: {url}")
        return pd.DataFrame()

    except ValueError:
        print(f"No tables found for: {url}")
        return pd.DataFrame()

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return pd.DataFrame()


def create_cache_from_scraped_data():
    CACHE_DIR.mkdir(exist_ok=True)

    cached_data = {}

    for name, url in URLS.items():
        st.write(f"Scraping {name} data...")

        df = scrape_table(url)

        if df.empty:
            st.write(f"Skipping {name} because no table was found.")
            continue

        cached_data[name] = df

        with open(INDIVIDUAL_CACHE_FILES[name], "wb") as file:
            pickle.dump(df, file)

    with open(PROJECT_CACHE_FILE, "wb") as file:
        pickle.dump(cached_data, file)

    return cached_data


def load_project_cache():
    CACHE_DIR.mkdir(exist_ok=True)

    if PROJECT_CACHE_FILE.exists():
        with open(PROJECT_CACHE_FILE, "rb") as file:
            return pickle.load(file)

    return create_cache_from_scraped_data()


def prepare_all_data():
    raw_tables = load_project_cache()

    if len(raw_tables) == 0:
        st.error("No data was scraped. Check the URLs or try again later.")
        return {}

    cleaned_tables = {}

    for name, df in raw_tables.items():
        cleaned_df = df.copy()

        cleaned_df = cleaned_df.dropna(how="all")

        cleaned_tables[name] = cleaned_df

    return cleaned_tables

def combine_tables(cleaned_tables):
    all_data = []

    for name, df in cleaned_tables.items():
        all_data.append(df)

    if len(all_data) == 0:
        return pd.DataFrame()

    combined = pd.concat(all_data, ignore_index=True)
    combined["Indicator"] = combined["Indicator"].str.replace("_", " ").str.title()

    return combined


def make_line_chart(data):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=data, x="Year", y="Value", hue="Indicator", marker="o", ax=ax)
    ax.set_title("Economic Indicators Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Value")
    st.pyplot(fig)


def make_bar_chart(data):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=data, x="Year", y="Value", hue="Indicator", ax=ax)
    ax.set_title("Economic Indicators by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Value")
    plt.xticks(rotation=45)
    st.pyplot(fig)


def main():
    st.title("Economic Indicators by U.S. President")

    st.write(
        "This app separates scraped economic data by president. "
        "Use the dropdowns to choose a presidency and compare different visuals."
    )

    cleaned_tables = prepare_all_data()
    combined_data = combine_tables(cleaned_tables)

    if combined_data.empty:
        st.error("No data was loaded. Check your project_cache folder or scraped data.")
        return

    president_options = sorted(combined_data["President"].dropna().unique())

    selected_president = st.selectbox(
        "Choose a president:",
        president_options
    )

    president_data = combined_data[
        combined_data["President"] == selected_president
    ]

    indicator_options = sorted(president_data["Indicator"].dropna().unique())

    selected_indicators = st.multiselect(
        "Choose economic indicators to compare:",
        indicator_options,
        default=indicator_options
    )

    visual_choice = st.selectbox(
        "Choose a visual:",
        ["Line Chart", "Bar Chart", "Data Table"]
    )

    filtered_data = president_data[
        president_data["Indicator"].isin(selected_indicators)
    ]

    st.subheader(f"Data for {selected_president}")

    if filtered_data.empty:
        st.warning("No data available for this selection.")
        return

    party = filtered_data["Party"].iloc[0]
    start_year = filtered_data["Year"].min()
    end_year = filtered_data["Year"].max()

    st.write(f"Party: {party}")
    st.write(f"Years in dataset: {start_year} - {end_year}")

    if visual_choice == "Line Chart":
        make_line_chart(filtered_data)

    elif visual_choice == "Bar Chart":
        make_bar_chart(filtered_data)

    elif visual_choice == "Data Table":
        st.dataframe(filtered_data)

    st.subheader("Summary Statistics")
    summary = (
        filtered_data
        .groupby("Indicator")["Value"]
        .agg(["mean", "min", "max"])
        .reset_index())

    st.dataframe(summary)


if __name__ == "__main__":
    main()

# this project was lowkey diffucalt in trying to scrap the data. At first I was going to downlaod the file 
# but I w think the website changed it so the uaer cant downlaod it but i just scraped it insted of downloading the the file .
#given the fact that data can chnage over time
#I also used chat gpt to help me teh time max out error, and the indivusla cache 
#This project helped me better understand how ETL pipelines work from start to finish. 
# I learned how to extract data from websites using Playwright, transform the data with pandas.
# The most difficult part of the project was dealing with unreliable website data and preventing the program from crashing. 
# I solved this by using try/except blocks and 
# checking for empty DataFrames before continuing the pipeline.
