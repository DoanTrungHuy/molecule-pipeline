from pydantic import BaseModel
from typing import List

class Filters(BaseModel):
    mw: float
    logp: float
    hbd: int
    hba: int
    tpsa: float
    max_violations: int

class RunRequest(BaseModel):
    objective: str
    seeds: List[str]
    filters: Filters
    num_candidates: int
    rounds: int
    top_k: int
