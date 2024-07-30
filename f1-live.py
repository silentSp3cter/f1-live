from urllib.request import urlopen
import json
import pandas as pd

input_string = str(input('GP; Year; Session; Seperate with ;'))
gp = input_string.split(";")[0].strip()
year = input_string.split(";")[1].strip()
session = input_string.split(";")[2].strip()
print(gp, year, session)