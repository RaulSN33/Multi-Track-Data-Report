import matplotlib.pyplot as plt

from src.DataClass import ByTermStudentData
from src.DataLoader import DataLoader, subjects
from src.ploting import histograms
import seaborn as sns
import pandas as pd


route = 'Input'
loader = DataLoader(route)


#%%

loader.get_data()

data = loader.data
# data['student_grades_2027-2028']

described_fall = data['2027-2028']['Fall'].df.describe()
described_spring = data['2027-2028']['Spring'].df.describe()

#%%


# histograms(
#     data[],
#     '2027-2028'
# )

#%%

# df = data['student_grades_2027-2028'].df

# first_term = df[df['Term']==1]
# second_term = df[df['Term']==2]
# summary_avg1 = first_term[subjcts+['Track', 'IncomeStudent']].groupby(['Track','IncomeStudent']).mean()
# summary_avg2 = second_term[subjcts+['Track', 'IncomeStudent']].groupby(['Track','IncomeStudent']).mean()

#%%

def avg_by_track_income(data,year):
    first_term = data[year]['Fall'].df
    second_term = data[year]['Spring'].df

    summary_avg1 = first_term[subjects+['Track', 'IncomeStudent']].groupby(['Track','IncomeStudent']).mean()
    summary_avg2 = second_term[subjects+['Track', 'IncomeStudent']].groupby(['Track','IncomeStudent']).mean()

    return summary_avg1, summary_avg2

summary_avg1, summary_avg2 = avg_by_track_income(data, '2027-2028')


#%%

def average_grades(
        groupby_summaries,
        plot_title
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


average_grades(
    groupby_summaries=summary_avg1,
    plot_title = 'Fall Term; Average grades by track'

)

average_grades(
    groupby_summaries=summary_avg2,
    plot_title = 'Spring Term; Average grades by track'

)
#%%
df_to_plot = summary_avg2.T
df_to_plot.columns = df_to_plot.columns.set_levels(['Local','Incoming'],level=1)
tracks = df_to_plot.columns.get_level_values(0).unique()

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 9), sharey=True)

fig.suptitle('Term 2; Average Grades by Track', fontweight = 'bold')

for i, track in enumerate(tracks):
    df_to_plot[track].plot.bar(ax=axes[i])
    axes[i].grid(axis='y')
    axes[i].set_title(track)
    axes[i].tick_params(axis='x', labelrotation=0)
    axes[i].legend(loc='lower left')

sns.despine()
plt.tight_layout()
plt.show()

#%%

# Assuming df is already loaded as in your code
df = data['student_grades_2027-2028'].df

# Step 1: Aggregate — count number of Pass vs Fail by Track and IncomeStudent

summary_passfail = (
    first_term.groupby(['Track', 'IncomeStudent', 'Passed (Y/N)'])
      .size()
      .reset_index(name='Count')
)

# Step 2: For plotting convenience, pivot table
pivot_data = summary_passfail.pivot_table(
    index=['Track', 'IncomeStudent'],
    columns='Passed (Y/N)',
    values='Count',
    fill_value=0
).reset_index()

# Step 3: Prepare figure with 3 pie charts (one per track)
tracks = pivot_data['Track'].unique()
fig, axes = plt.subplots(1, len(tracks), figsize=(15, 6))
fig.suptitle('Pass vs Fail Distribution by Track', fontsize=16, fontweight='bold')

# Step 4: Plot pie chart for each track
for i, track in enumerate(tracks):
    ax = axes[i]
    track_data = (
        first_term[first_term['Track'] == track]['Passed (Y/N)']
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

#%%
# Assuming df is already loaded as in your code
df = data['student_grades_2027-2028'].df

# Step 1: Aggregate — count number of Pass vs Fail by Track and IncomeStudent

summary_passfail = (
    second_term.groupby(['Track', 'IncomeStudent', 'Passed (Y/N)'])
      .size()
      .reset_index(name='Count')
)

# Step 2: For plotting convenience, pivot table
pivot_data = summary_passfail.pivot_table(
    index=['Track', 'IncomeStudent'],
    columns='Passed (Y/N)',
    values='Count',
    fill_value=0
).reset_index()

# Step 3: Prepare figure with 3 pie charts (one per track)
tracks = pivot_data['Track'].unique()
fig, axes = plt.subplots(1, len(tracks), figsize=(15, 6))
fig.suptitle('Pass vs Fail Distribution by Track', fontsize=16, fontweight='bold')

# Step 4: Plot pie chart for each track
for i, track in enumerate(tracks):
    ax = axes[i]
    track_data = (
        second_term[second_term['Track'] == track]['Passed (Y/N)']
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