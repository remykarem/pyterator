from typing import Optional
from pyterator import iterate

text = """Survived,Pclass,Name,Sex,Age,Siblings/Spouses Aboard,Parents/Children Aboard,Fare
0,3,Mr+ Owen Harris Braund,male,22,1,0,7.25
1,3,Miss. Laina Heikkinen,female,26,0,0,7.925
1,1,Mrs. Jacques Heath (Lily May Peel) Futrelle,female,35,1,0,53.1
0
0,3,Mr. James Moran,male,27,0,0,8.4583
0,1,Mr. Timothy J McCarthy,male,54,0,0,51.8625
0,3,Master. Gosta Leonard Palsson,male,2,3,1,21.075
1,3,Mrs. Oscar W (Elisabeth Vilhelmina Berg) Johnson,female,27,0,2,11.1333
1,1,Miss+ Elizabeth Bonnell,female,58,0,0,26.55
0,3,Mr. William Henry Saundercock,male,20,0,0,8.05"""


def get_name_from_line(line: str) -> Optional[str]:
    # We can use the walrus operator here
    name = line.split(",")[2:3]
    if name:
        return name[0]
    else:
        return None
    
def get_name_split(name: str) -> Optional[list]:
    # We can use the walrus operator here
    split = name.split(". ")
    if len(split) == 2:
        return split
    else:
        return None

title_names: dict = (
    iterate(text.split("\n"))
    .filter_map(get_name_from_line)
    .filter_map(get_name_split)
    .groupby(lambda name: name[0], lambda name: name[1])
)
