# currency-rate

**Hands-on experiments with real-world currency exchange-rate data**
A compact Python project exploring data extraction, parsing, and lightweight analytics for fiat and crypto currencies.
Focused on clean modular code, Poetry-based packaging, and CLI usability.

---

## 🧬 Motivation

This repository serves as a sandbox for experimenting with:
- data ingestion from public FX and crypto APIs,
- data normalization and formatting logic,
- quick visual or tabular outputs suitable for bots, dashboards, or notebooks.

It uses data from real websites I check daily to monitor both fiat and crypto exchange rates, collected automatically through the Telegram bot, which is deployed on Render.com as a webhook service. The project intentionally keeps minimal external dependencies to stay portable and test automation-ready.

---

## ⚙️ Features

* **Unified CLI tool:** fetches current fiat and crypto exchange rates.
* **Structured codebase:** clear separation between extraction, formatting, and presentation.
* **Environment-driven configuration:** `.env` support for API keys or environment overrides.
* **Poetry integration:** clean dependency management and virtualenv isolation.
* **Optional Telegram bot extension:** early experiments with interactive rate retrieval.

---

## 🗂️ Repository structure

```
├── cyrates/
│   ├── bot/                # Telegram bot logic (async handlers, menus, commands)
│   ├── parsing/            # API clients, formatters, and rate extractors
│   └── __init__.py
│
├── notebooks/              # Jupyter notebooks for exploratory FX analysis
├── tests/                  # Unit tests (pytest)
├── pyproject.toml          # Poetry configuration
├── .env.example            # Template for environment variables
└── README.md
```

---

## 🚀 Quick start

### Requirements

* Python ≥ 3.11
* Poetry
* .env file for API keys containing the following variables:
  * `OPENAI_API_KEY`
  * `TELEGRAM_BOT_TOKEN`
  * `TELEGRAM_BOT_MODE` (webhook or polling)
  * `WEBHOOK_PORT` (usually 8080)
  * `WEBHOOK_URL`

### Installation

Repo-installation
```bash
git clone https://github.com/povodmax/currency-rate.git
cd currency-rate
poetry install
```
Kernel-installation for jupiter notebooks:
`poetry run python -m ipykernel install --user --name=currency-rate --display-name="currency-rate Python 3.11 (Poetry)"`

## 📚 Examples

* See `notebooks/_dev_.ipynb` for quick data exploration examples.
* Or run the main CLI tool:
```bash
poetry run rates
```

---

## 🧬 Tech stack

| Layer           | Technology            |
| --------------- | --------------------- |
| Language        | Python 3.11           |
| Package manager | Poetry                |
| API clients     | `requests`            |
| CLI             | built-in `argparse`   |
| Env management  | `python-dotenv`       |
| Bot             | `python-telegram-bot` |

---

## 🤪 Development & Testing

Run linters/formatters (ruff) and tests (pytest):

```bash
poetry run pre-commit run --all-files
poetry run pytest
```

---

## 🤝 Contributing

Pull requests are welcome — focus on modularity, typing, and minimal dependencies.
For new ideas, open an issue or a draft PR.

---

## 📜 License

[Max Povod](https://github.com/povodmax)

---

## 📨 Contact

**Author:** [Max Povod](https://www.linkedin.com/in/povodmax/)
**Focus:** Data Science / ML Engineering / Supply Chain Analytics
