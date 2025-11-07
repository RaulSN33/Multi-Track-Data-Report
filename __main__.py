import matplotlib.pyplot as plt

from src.DataClass import AnnualStudentData
from src.DataLoader import DataLoader
from src.ploting import histograms
import seaborn as sns
import pandas as pd


route = 'Input'
loader = DataLoader(route)


#%%

data = loader.get_data()
# data['student_grades_2027-2028']

described = data['student_grades_2027-2028'].df.describe()

#%%


histograms(
    data,
    'student_grades_2027-2028'
)

#%%

df = data['student_grades_2027-2028'].df
subjcts = [
    'Math',
    'English',
    'Science',
    'History'
]

summary_avg = df[subjcts+['Track', 'IncomeStudent']].groupby(['Track','IncomeStudent']).mean()
