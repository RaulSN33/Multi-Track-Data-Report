import dataclasses
import pandas as pd

@dataclasses.dataclass
class AnnualStudentData:
    df: pd.DataFrame
    subjects: list


