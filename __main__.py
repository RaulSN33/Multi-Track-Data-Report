import matplotlib.pyplot as plt

from src.DataLoader import DataLoader
from src.DataWrangling import (
    avg_by_track_income,
    pass_vs_fail_analytics
)

from src.helpers import terms_mapping_dict

from src.ploting import (
    average_grades,
    histograms,
    pct_passed_pie
)
import seaborn as sns

route = 'Input'
loader = DataLoader(route)


#%%

loader.get_data()

data = loader.data
# data['student_grades_2027-2028']

described_fall = data['2027-2028']['Fall'].df.describe()
described_spring = data['2027-2028']['Spring'].df.describe()

#%%


histograms(
    data,
    '2027-2028',
    terms=['Fall', 'Spring']
)



#%%


summary_avg1, summary_avg2 = avg_by_track_income(data, '2027-2028')

#
average_grades(
    groupby_summaries=summary_avg1,
    plot_title = 'Fall Term; Average grades by track'

)

average_grades(
    groupby_summaries=summary_avg2,
    plot_title = 'Spring Term; Average grades by track'

)


#%%

pass_fail_dict_results = pass_vs_fail_analytics(
    data,
    year='2027-2028',
    terms=['Fall', 'Spring']
)

#%%
for _, term in terms_mapping_dict.items():
    pct_passed_pie(
        pass_fail_dict_results[term],
        data['2027-2028'][term].df
    )
