from pyterator import iterate

cipher = "rovzwo"
clear = (
    iterate(cipher)
    .map(ord)
    .map("-", 10)
    .map(chr)
    .join()
)
assert clear == "helpme"
