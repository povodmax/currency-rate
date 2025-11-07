import typing as tp
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd


def display_as_image(df: pd.DataFrame) -> BytesIO:

    fig, ax = plt.subplots(figsize=(1, 1), dpi=300)
    ax.axis("tight")
    ax.axis("off")

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
        cellLoc="right",
    )

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("black")  # black borders
        if row == 0:  # only 1st row - headlines
            cell.set_text_props(weight="bold", color="black")  # bold text
            cell.set_facecolor("#d9edf7")  # light-blue background

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.auto_set_column_width(col=list(range(len(df.columns))))

    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight", pad_inches=0.2)
    buffer.seek(0)
    plt.close(fig)

    return buffer


def pretty_print(df: pd.DataFrame, as_what: str) -> tp.Optional[tp.Union[BytesIO, str]]:
    """
    Parameter as_what can be:
        - "text"
        - "image"
        - "markdown"
        - "csv"
    """
    if as_what == "text":
        return df.to_string(index=False)
    elif as_what == "image":
        return display_as_image(df)
    else:
        return None
