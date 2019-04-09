from enum import Enum

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class ToolModes(Enum):
    MoveMode = 1
    CorrosionMode = 2
    ReportMode = 3
    AutoDetectMode = 4
    RefSelectionMode = 5

class ReportTools(Enum):
    K = 0
    L = 1
    SP = 2
    SW = 3
