from typing import Dict, Optional, Any
from pydantic.dataclasses import dataclass



@dataclass(config=dict(arbitrary_types_allowed=True))
class BaseModelregistry:
    registry: Optional[Dict[str, Any]] = None