import dataclasses
import pandas as pd

@dataclasses.dataclass
class ByTermStudentData:
    df: pd.DataFrame
    subjects: list


