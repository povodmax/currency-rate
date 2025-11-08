import pytest
from unittest.mock import patch, Mock
import pandas as pd

from cyrates.parsing.extractor import CurrencyExtractor


MOCK_TABLE_HTML = """
<table>
<tr><th>Букв. код</th><th>Единиц</th><th>Валюта</th><th>Курс</th></tr>
<tr><td>USD</td><td>1</td><td>Доллар США</td><td>93,25</td></tr>
<tr><td>EUR</td><td>1</td><td>Евро</td><td>98,40</td></tr>
</table>
"""

@pytest.fixture
def extractor():
    return CurrencyExtractor()

def test_format_crypto_price_low(extractor):
    assert extractor.format_crypto_price(88.88) == "88.88 $"

def test_format_crypto_price_high(extractor):
    assert extractor.format_crypto_price(1234.56) == "1 234 $"

@patch("cyrates.parsing.extractor.CurrencyExtractor.get_classdata_from_url")
@patch("pandas.read_html")
def test_get_cbr_fiat_rates(mock_read_html, mock_get_classdata, extractor):
    mock_get_classdata.return_value = MOCK_TABLE_HTML
    df_mock = pd.DataFrame({
        "Букв. код": ["USD", "EUR"],
        "Единиц": [1, 1],
        "Валюта": ["Доллар", "Евро"],
        "Курс": ["93,25", "98,40"],
    })
    mock_read_html.return_value = [df_mock]

    df = extractor.get_cbr_fiat_rates(["USD"])
    assert not df.empty
    assert list(df.columns) == ["code", "rate", "source"]
    assert df["code"].iloc[0] == "USD"
    assert df["rate"].iloc[0].endswith("₽")

@patch("requests.get")
def test_get_freedom_fiat_rates(mock_get, extractor):
    mock_get.return_value = Mock(status_code=200)
    mock_get.return_value.json.return_value = {
        "data": {
            "mobile": [
                {"buyCode": "USD", "sellCode": "RUB", "buyRate": "93,50", "sellRate": "94,00"},
                {"buyCode": "EUR", "sellCode": "RUB", "buyRate": "98,00", "sellRate": "99,00"},
            ]
        }
    }

    df = extractor.get_freedom_fiat_rates()
    assert not df.empty
    assert set(df.columns) == {"code", "rate", "source"}
    assert "USD" in df["code"].values
    assert df["rate"].str.endswith("₽").all()
