from config import *
from myscript import Scripter, DBHandler

scripter = Scripter(SCENARIO_MAP, DB_PATH)

scripter.setup_script()
info = scripter.respond('sample', 0, 'hello', trial=3)
print(info)
# data = scripter.check_answer('I am sleepy', ['How much is it?', 'I am tired'])

# data = scripter.


# dh = DBHandler(DB_PATH)
# data = dh.get_vectorized_by_sentence(['How much is it?'])
# print(data)