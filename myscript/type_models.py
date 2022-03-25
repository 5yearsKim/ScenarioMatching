from pydantic import BaseModel
from typing import Any, Optional

class Sentence(BaseModel):
    id: int
    sentence: str
    vector: Optional[bytes]

class ScriptInfo(BaseModel):
    title: str
    description: str
    npc_name: str
    npc: str

class ScriptIn(BaseModel):
    script_id: str
    turn_idx: int = 0
    trial: int = 0
    answer: str

class ScriptOut(BaseModel):
    is_success: bool = False
    answer: str
    hint: Optional[str]
    npc: Optional[str]
    is_end: bool = False