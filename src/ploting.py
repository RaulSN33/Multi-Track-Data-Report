import seaborn as sns
import matplotlib.pyplot as plt
from src.DataClass import ByTermStudentData

def histograms(data: ByTermStudentData, file_to_plot):
    df = data[file_to_plot].df.copy()
    # a = pd.pivot(
    #     data=data.data,
    #     values='ProjectScore',
    #     index='StudentID',
    #     columns='Track'
    # )

    tracks_to_plot = ['Data', 'BM', 'Finance']

    for track in tracks_to_plot:
        plt.hist(
            df.loc[df['Track']==track, 'ProjectScore'],
            bins = 50,
            label = track,
            alpha = 0.8,
        )
    sns.despine()
    plt.grid(alpha=0.5)
    plt.legend()
    plt.show()

