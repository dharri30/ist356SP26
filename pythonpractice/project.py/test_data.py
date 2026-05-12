
'''Function TEst''''''

import pandas as pd
from pathlib import Path
import pickle

import data



def test_scrape_table_handles_no_tables(monkeypatch):
    def fake_read_html(html):
        raise ValueError("No tables found")

    monkeypatch.setattr(data.pd, "read_html", fake_read_html)

    result = data.scrape_table("https://fake-url.com")

    assert isinstance(result, pd.DataFrame)
    assert result.empty


def test_create_cache_skips_empty_dataframe(monkeypatch, tmp_path):
    fake_urls = {
        "unemployment": "https://fake-url.com"
    }

    empty_df = pd.DataFrame()

    monkeypatch.setattr(data, "URLS", fake_urls)
    monkeypatch.setattr(data, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(data, "PROJECT_CACHE_FILE", tmp_path / "project_cache.pkl")
    monkeypatch.setattr(
        data,
        "INDIVIDUAL_CACHE_FILES",
        {"unemployment": tmp_path / "unemployment.pkl"}
    )

    monkeypatch.setattr(data, "scrape_table", lambda url: empty_df)

    result = data.create_cache_from_scraped_data()

    assert result == {}
    assert (tmp_path / "project_cache.pkl").exists()


def test_load_project_cache_existing_file(monkeypatch, tmp_path):
    fake_data = {
        "unemployment": pd.DataFrame({
            "Year": [2020],
            "Rate": [8.1]
        })
    }

    cache_file = tmp_path / "project_cache.pkl"

    with open(cache_file, "wb") as file:
        pickle.dump(fake_data, file)

    monkeypatch.setattr(data, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(data, "PROJECT_CACHE_FILE", cache_file)

    result = data.load_project_cache()

    assert "unemployment" in result
    assert isinstance(result["unemployment"], pd.DataFrame)


def test_load_project_cache_creates_cache_if_missing(monkeypatch, tmp_path):
    fake_data = {
        "unemployment": pd.DataFrame({
            "Year": [2020],
            "Rate": [8.1]
        })
    }

    monkeypatch.setattr(data, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(data, "PROJECT_CACHE_FILE", tmp_path / "missing_cache.pkl")
    monkeypatch.setattr(data, "create_cache_from_scraped_data", lambda: fake_data)

    result = data.load_project_cache()

    assert "unemployment" in result


def test_prepare_all_data(monkeypatch):
    fake_raw_tables = {
        "unemployment": pd.DataFrame({
            "Year": [2020, 2021, None],
            "Rate": [8.1, 5.4, None]
        })
    }

    monkeypatch.setattr(data, "load_project_cache", lambda: fake_raw_tables)

    result = data.prepare_all_data()

    assert "unemployment" in result
    assert isinstance(result["unemployment"], pd.DataFrame)
    assert len(result["unemployment"]) == 2


def test_prepare_all_data_empty_cache(monkeypatch):
    monkeypatch.setattr(data, "load_project_cache", lambda: {})

    result = data.prepare_all_data()

    assert result == {}