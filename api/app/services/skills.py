from typing import Any, Callable, Dict, List, Optional, TypedDict
import functools
import logging
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class SkillMetadata(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)

class SkillRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SkillRegistry, cls).__new__(cls)
            cls._instance._skills = {}
        return cls._instance

    def register(self, name: str, description: str, parameters: Optional[Dict[str, Any]] = None):
        def decorator(func: Callable):
            self._skills[name] = {
                "func": func,
                "metadata": SkillMetadata(name=name, description=description, parameters=parameters or {})
            }
            return func
        return decorator

    def execute(self, name: str, args: Dict[str, Any]) -> Any:
        if name not in self._skills:
            raise ValueError(f"Skill '{name}' not found in registry")

        logger.info(f"Executing skill: {name} with args: {args}")
        try:
            return self._skills[name]["func"](**args)
        except Exception as e:
            logger.error(f"Error executing skill {name}: {str(e)}")
            return f"Error executing skill {name}: {str(e)}"

    def get_all_schemas(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": meta.name,
                    "description": meta.description,
                    "parameters": {
                        "type": "object",
                        "properties": meta.parameters,
                        "required": list(meta.parameters.keys())
                    }
                }
            }
            for meta in [s["metadata"] for s in self._skills.values()]
        ]

registry = SkillRegistry()
skill = registry.register
