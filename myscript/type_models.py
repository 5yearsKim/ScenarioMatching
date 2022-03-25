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

class SentenceScore(BaseModel):
    compare: str
    sentence: str
    score: Optional[float]

class ScriptOut(BaseModel):
    is_success: bool = False
    turn_idx: int
    npc: str
    last_answer: Optional[SentenceScore]
    hint: Optional[str]
    is_end: bool = False

