from config import *
from myscript import Scripter

scripter = Scripter(SCENARIO_MAP, DB_PATH)

info = scripter.respond('sample', 0, 'hello')
print(info)