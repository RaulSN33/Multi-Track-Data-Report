import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from numpy import histogram_bin_edges
from src.DataClass import ByTermStudentData
from src.helpers import tracks


def histograms(
        data: ByTermStudentData,
        year_to_plot: str,
        terms: str,
        tracks=tracks
):
    yearly_info = data[year_to_plot]
    tracks_to_plot = tracks

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(9, 8), sharex=True)

    for idx, term in enumerate(terms):
        df_to_plot = yearly_info[term].df

        # bins across all tracks for each term
        all_scores = df_to_plot['ProjectScore']
        bins = histogram_bin_edges(all_scores, bins=18)

        for track in tracks_to_plot:
            axes[idx].hist(
                df_to_plot.loc[df_to_plot['Track'] == track, 'ProjectScore'],
                bins=bins,
                label=track,
                alpha=0.5,
                edgecolor='black'
            )

        axes[idx].set_title(f'{term} term')
        axes[idx].grid(alpha=0.5)
        sns.despine(ax=axes[idx])

    fig.suptitle(f'Year {year_to_plot} scores', fontweight = 'bold')
    axes[0].legend()
    plt.tight_layout()
    plt.show()
    return fig

def average_grades(
        groupby_summaries: pd.DataFrame,
        plot_title: str
):

    df_to_plot = groupby_summaries.T
    df_to_plot.columns = df_to_plot.columns.set_levels(['Local','Incoming'],level=1)
    tracks = df_to_plot.columns.get_level_values(0).unique()

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 7), sharey=True)

    fig.suptitle(plot_title, fontweight = 'bold')

    for i, track in enumerate(tracks):
        df_to_plot[track].plot.bar(ax=axes[i])
        axes[i].grid(axis='y')
        axes[i].set_title(track)
        axes[i].tick_params(axis='x', labelrotation=0)
        axes[i].legend(loc='lower left')

    sns.despine()
    plt.tight_layout()
    plt.show()
    return fig

def pct_passed_pie(
        pass_fail_info,
        term_info,
        title
):
    tracks = pass_fail_info['Track'].unique()
    fig, axes = plt.subplots(1, len(tracks), figsize=(13, 5))
    fig.suptitle(title, fontsize=16, fontweight='bold')

    # Step 4: Plot pie chart for each track
    for i, track in enumerate(tracks):
        ax = axes[i]
        track_data = (
            term_info[term_info['Track'] == track]['Passed (Y/N)']
            .value_counts()
            .reindex(['Y', 'N'], fill_value=0)
        )

        ax.pie(
            track_data,
            labels=['Passed', 'Failed'],
            autopct='%1.1f%%',
            startangle=90,
            colors=['#4CAF50', '#F44336']
        )
        ax.set_title(track)

    sns.despine()
    plt.tight_layout()
    plt.show()
    return fig


def by_subject_boxplot(
        df_to_plot: pd.DataFrame,
        subject: str,
        term: str,
        year: str,
):
# b = data['2027-2028']['Spring'].df
    df_to_plot['IncomeStudent'] = df_to_plot['IncomeStudent'].replace({0:'Local', 1:'Foreigner'})

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 7), sharey=True)
    sns.boxplot(
        data = df_to_plot,
        x='Track',
        y=subject,
        color = 'green',
        ax = axes[0]

    )
    sns.boxplot(
        data = df_to_plot,
        x = 'Track',
        y=subject,
        hue='IncomeStudent',
        ax = axes[1]

    )
    axes[1].legend(loc='lower left')
    sns.despine()
    fig.suptitle(f'{year}, {term}; {subject} Scores')
    plt.tight_layout()
    plt.show()

    return fig
