"""
Example taken from
https://realpython.com/introduction-to-python-generators/
"""
from pyterator import iterate


text = """permalink,company,numEmps,category,city,state,fundedDate,raisedAmt,raisedCurrency,round
digg,Digg,60,web,San Francisco,CA,1-Dec-06,8500000,USD,b
digg,Digg,60,web,San Francisco,CA,1-Oct-05,2800000,USD,a
facebook,Facebook,450,web,Palo Alto,CA,1-Sep-04,500000,USD,angel
facebook,Facebook,450,web,Palo Alto,CA,1-May-05,12700000,USD,a
photobucket,Photobucket,60,web,Palo Alto,CA,1-Mar-05,3000000,USD,a"""

data = (
    iterate(text.split("\n"))
    .map(lambda s: s.split(","))
    .to_gen()
)

header = next(data)

ans = (
    iterate(data)
    .flat_map(lambda row: zip(header, row))
    .groupby(lambda x: x[0], lambda x: x[1])
)

assert ans['permalink'] == ['digg',
                            'digg',
                            'facebook',
                            'facebook',
                            'photobucket']
