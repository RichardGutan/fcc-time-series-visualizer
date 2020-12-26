import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', delimiter=',')
df.index = [pd.Timestamp(d) for d in df.index]

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots()
    ax.plot('value', data=df)
    ax.set_ylabel('Page Views')
    ax.set_xlabel('Date')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = [d.year for d in df_bar.index]
    df_bar['month'] = [d.month_name() for d in df_bar.index]
    df_bar['monthNumber'] = [d.month for d in df_bar.index]
    
    years = df_bar['year'].unique()
    months = df_bar.sort_values('monthNumber')['month'].unique()

    df_bar2 = df_bar.groupby(['month', 'year']).mean()
    df_bar2 = df_bar2.reset_index()
    df_bar3 = df_bar2.pivot(index='month', columns='year', values='value')        

    x = np.arange(len(years))  # the label locations
    width = 1 / 24  # the width of the bars

    # Draw bar plot
    fig, ax = plt.subplots()
    
    for i in range(len(months)):
        ax.bar(x + width*i, df_bar3.loc[months[i]].values, width, label=months[i])
    
    ax.set_ylabel('Average Page Views')
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_xlabel('Years')
    ax.legend()


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box['year'] = [d.year for d in df_box.index]
    df_box['month'] = [d.strftime('%b') for d in df_box.index]
    df_box['monthNumber'] = [d.month for d in df_box.index]
    df_box = df_box.sort_values(by='monthNumber')

    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(ncols=2)
    sns.boxplot(x="year", y="value", ax=axs[0], data=df_box);
    sns.boxplot(x="month", y="value", ax=axs[1], data=df_box);

    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')
    axs[0].set_title('Year-wise Box Plot (Trend)')

    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')
    axs[1].set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
