# -*- coding: utf-8 -*-
import os
import typing as tp

import bs4
import numpy as np
import pandas as pd
import requests

from cyrates.agent.const import UrlCatalog


class CurrencyAgent:
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

    def get_fiat_rates(
        self,
        fiat_list: tp.List[str] = ["USD", "EUR", "KZT"],
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
        df["rate"] = np.round(df["currency_rate"], 2)
        return df[["code", "rate"]]

    def get_binance_crypto_rates(
        self,
        crypto_list: tp.List[str] = ["notcoin", "toncoin", "bitcoin"],
    ) -> pd.DataFrame:
        content = []
        for coin in crypto_list:
            tag_el = self.get_classdata_from_url(
                os.path.join(UrlCatalog.BINANCE, coin),
                "t-Caption2 text-textThird",
            )
            price = float(str(tag_el).split("$")[1].split("<")[0].replace(",", ""))
            price_formatted = "{:.4f} $".format(price) if price < 100 else "{:,d} $".format(int(price))
            content.append(
                (price_formatted, coin, "binance"),
            )
        return pd.DataFrame(content, columns=["price", "crypto", "source"])

    def get_rbc_crypto_rates(
        self,
        crypto_list: tp.List[str] = ["btcusd"],
    ) -> pd.DataFrame:
        content = []
        for coin in crypto_list:
            tag_el = self.get_classdata_from_url(
                os.path.join(UrlCatalog.RBC, coin),
                "chart__subtitle js-chart-value",
            )
            price = float(str(tag_el).split("\n")[1].replace(" ", ""))
            price_formatted = "{:.4f} $".format(price) if price < 100 else "{:,d} $".format(int(price))
            content.append(
                (price_formatted, coin, "rbc"),
            )
        return pd.DataFrame(content, columns=["price", "crypto", "source"])

    def get_crypto_rates(self) -> pd.DataFrame:
        crypto_rates = [
            self.get_binance_crypto_rates(),
            self.get_rbc_crypto_rates(),
        ]
        return pd.concat(crypto_rates)
