from typing import Dict, Optional, Any
from pydantic.dataclasses import dataclass



@dataclass(config=dict(arbitrary_types_allowed=True))
class BaseToolregistry:
    registry: Optional[Dict[str, Any]] = None