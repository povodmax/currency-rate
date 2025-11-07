# -*- coding: utf-8 -*-
import os
import typing as tp

import bs4
import numpy as np
import pandas as pd
import requests

from cyrates.parsing.const import UrlCatalog


class CurrencyExtractor:
    """Gets currency data from various sources."""

    def __init__(self):
        pass

    def get_classdata_from_url(
        self,
        url_adress: str,
        class_we_searching: str,
    ) -> bs4.element.Tag:
        response = requests.get(url_adress)  # get HTML-code for page
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        return soup.find(class_=class_we_searching)
    
    @staticmethod   
    def format_crypto_price(price: float, currency_sign: str = "$") -> str:
        """Format float price for cryptos with dollar sign and thousands separator."""
        if price < 100:
            return f"{price:.2f} {currency_sign}"
        return f"{int(price):,}".replace(",", " ") + f" {currency_sign}"

    def get_cbr_fiat_rates(
        self,
        fiat_list: tp.List[str] = ["USD", "EUR", "KZT", "CNY", "TRY", "AED"],
    ) -> pd.DataFrame:
        tag_el = self.get_classdata_from_url(UrlCatalog.CBR, "table")
        rnm_dict = {
            "Букв. код": "code",
            "Единиц": "num",
            "Валюта": "currency",
            "Курс": "currency_rate",
        }
        df = pd.read_html(str(tag_el), converters={4: str}, thousands=None)[0]
        df = df.rename(columns=rnm_dict)
        df = df.loc[df["code"].isin(fiat_list)]
        df["currency_rate"] = df["currency_rate"].apply(lambda x: float(x.replace(",", ".")))
        df["currency_rate"] = df.apply(
            lambda row: (row.num / row.currency_rate if row.num > 1 else row.currency_rate),
            axis=1,
        )
        df["rate"] = np.round(df["currency_rate"], 2).apply(lambda x: f"{x} ₽")
        df["source"] = "cbr"
        return  df[["code", "rate", "source"]]

    def get_freedom_fiat_rates(self) -> pd.DataFrame:
        
        def extract_non_rub_currency(pair: str) -> str:
            parts = pair.split(" / ")
            return parts[0] if parts[1] == "RUB" else parts[1]

        try:
            response = requests.get(UrlCatalog.FREEDOM)
            response.raise_for_status()
            data = response.json()

            items = data["data"]["mobile"]  # или "cash" / "nonCash"

            result = []
            for item in items:
                currency = f"{item['buyCode']} / {item['sellCode']}"
                buy = float(item["buyRate"].replace(",", "."))
                sell = float(item["sellRate"].replace(",", "."))
                result.append((currency, buy, sell))

            df = pd.DataFrame(result, columns=["currency", "buy", "sell"])
            df = df.loc[df["currency"].str.contains("RUB")]
            df["code"] = df["currency"].apply(extract_non_rub_currency)
            df["rate"] = df[["buy", "sell"]].max(axis=1).apply(lambda x: f"{x} ₽")
            df["source"] = "freedom"
            return df[["code", "rate", "source"]]

        except Exception as e:
            raise RuntimeError(f"Failed to fetch Freedom Bank rates: {e}")

    def get_bybit_crypto_rates(
        self, symbols: 
        tp.List[str] = ["BTC", "TON", "SOL", "ETH"],
    ) -> pd.DataFrame:
        """Fetches latest prices for selected crypto symbols from Bybit API."""
        
        try:
            response = requests.get(UrlCatalog.BYBIT, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            result = []
            for item in data.get("result", {}).get("list", []):
                symbol = item["symbol"]  # e.g. "BTCUSDT"
                for coin in symbols:
                    if symbol == f"{coin}USDT":
                        price = float(item["lastPrice"])
                        price_formatted = self.format_crypto_price(price)
                        result.append((coin, price_formatted, "bybit"))
            
            return pd.DataFrame(result, columns=["crypto", "price", "source"])
        
        except Exception as e:
            raise RuntimeError(f"Failed to fetch Bybit rates: {e}")

    def get_binance_crypto_rates(
        self, 
        symbols=["BTC", "ETH", "TON", "SOL"],
    ) -> pd.DataFrame:
        """Fetches latest prices for selected crypto symbols from Binance API."""

        try:
            response = requests.get(UrlCatalog.BINANCE, timeout=5)
            response.raise_for_status()
            data = response.json()

            result = []
            for coin in symbols:
                pair = f"{coin}USDT"
                entry = next((item for item in data if item["symbol"] == pair), None)
                if entry:
                    price = float(entry["price"])
                    price_formatted = self.format_crypto_price(price)
                    result.append((coin, price_formatted, "binance"))

            return pd.DataFrame(result, columns=["crypto", "price", "source"])

        except Exception as e:
            raise RuntimeError(f"Failed to fetch Binance rates: {e}")
        
    def get_rbc_crypto_rates(
        self,
        crypto_list: tp.List[str] = ["btcusd", "ethusd", "tonusd", "solusd"]
    ) -> pd.DataFrame:
        content = []
        for coin in crypto_list:
            try:
                tag_el = self.get_classdata_from_url(
                    os.path.join(UrlCatalog.RBC, coin),
                    "chart__subtitle js-chart-value",
                )
                if not tag_el:
                    continue

                lines = tag_el.get_text().split("\n")
                if len(lines) < 2:
                    continue

                price_str = lines[1].replace(" ", "").replace(",", ".")
                price = float(price_str)
                price_formatted = self.format_crypto_price(price)

                content.append((coin.replace("usd", "").upper(), price_formatted, "rbc"))
            except Exception:
                continue

        return pd.DataFrame(content, columns=["crypto", "price", "source"])

    def get_crypto_rates(self) -> pd.DataFrame:
        crypto_rates = [
            self.get_bybit_crypto_rates(),
            self.get_rbc_crypto_rates(),
            self.get_binance_crypto_rates(),
        ]
        return (
            pd.concat(crypto_rates)
            .pivot(index="crypto", columns="source", values="price")
            .reset_index()
            .sort_values("crypto", ascending=True)
        )
    
    def get_fiat_rates(self) -> pd.DataFrame:
        fiat_rates = [
            self.get_cbr_fiat_rates(),
            self.get_freedom_fiat_rates(),
        ]
        return (
            pd.concat(fiat_rates)
            .pivot(index="code", columns="source", values="rate")
            .reset_index()
            .sort_values("code", ascending=False)
        )
            