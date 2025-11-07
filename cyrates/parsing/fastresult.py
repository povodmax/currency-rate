import warnings

from cyrates.parsing.extractor import CurrencyExtractor
from cyrates.parsing.prettyprint import pretty_print

warnings.simplefilter(action="ignore", category=FutureWarning)


def launch() -> None:
    agent = CurrencyExtractor()
    print(
        "\n",
        "The Central Bank of Russian Federation present currency rates:",
        "\n",
        pretty_print(agent.get_fiat_rates(), "text"),
        "\n",
        "\n",
        "Real-time cryptocurrency prices across various trading and exchange platforms:",
        "\n",
        pretty_print(agent.get_crypto_rates(), "text"),
        "\n",
    )
