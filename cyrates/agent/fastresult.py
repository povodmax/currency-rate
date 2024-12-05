import warnings

from cyrates.agent.handler import CurrencyAgent
from cyrates.agent.prettyprint import pretty_print

warnings.simplefilter(action="ignore", category=FutureWarning)


def launch() -> None:
    agent = CurrencyAgent()
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
