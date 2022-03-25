import language_tool_python
from pydantic import BaseModel

tool = language_tool_python.LanguageToolPublicAPI('en-US') 
# tool = language_tool_python.LanguageTool('en-US') 

class Correction(BaseModel):
    ruleId: str 
    message: str
    replacements: list
    offsetInContext: int 
    context: str 
    offset: int 
    errorLength: int
    category: str 
    ruleIssueType: str
    sentence: str


def grammer_check(sentence):
    def convert_return(match):
        return Correction(**match.__dict__)
    matches = tool.check(sentence)

    matches = list(map(convert_return, matches))
    return matches

if __name__ == "__main__":
    matches = grammer_check('hello, i am from delited')
    print(matches)