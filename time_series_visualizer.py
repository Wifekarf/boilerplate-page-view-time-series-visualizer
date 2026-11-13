
import calendar

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data
df = pd.read_csv(
    'fcc-forum-pageviews.csv',
    parse_dates=['date'],
    index_col='date'
)

# Clean data
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(
        df_line.index,
        df_line['value'],
        color='red',
        linewidth=1
    )

    ax.set_title(
        'Daily freeCodeCamp Forum Page Views 5/2016-12/2019'
    )
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    df_bar = df.copy()

    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    df_bar = (
        df_bar.groupby(['year', 'month'])['value']
        .mean()
        .unstack('month')
    )

    df_bar = df_bar.reindex(columns=range(1, 13))

    df_bar.columns = [
        calendar.month_name[m]
        for m in range(1, 13)
    ]

    fig, ax = plt.subplots(figsize=(10, 8))

    df_bar.plot(kind='bar', ax=ax)

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')

    # Save image and return fig
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)

    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    month_order = [
        calendar.month_abbr[m]
        for m in range(1, 13)
    ]

    fig, axes = plt.subplots(1, 2, figsize=(20, 7))

    # Year-wise Box Plot
    sns.boxplot(
        data=df_box,
        x='year',
        y='value',
        ax=axes[0]
    )

    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].set_ylim(0, 200000)

    tick_values = np.arange(0, 200001, 20000)
    axes[0].set_yticks(tick_values)
    axes[0].set_yticklabels(
        [str(int(v)) for v in tick_values]
    )

    # Month-wise Box Plot
    sns.boxplot(
        data=df_box,
        x='month',
        y='value',
        order=month_order,
        ax=axes[1]
    )

    axes[1].set_title(
        'Month-wise Box Plot (Seasonality)'
    )
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    fig.tight_layout()

    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig
