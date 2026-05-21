from typing import Any

from pydantic import BaseModel, ConfigDict


class DecisionRecord(BaseModel):
    """Typed record of a decision, its reasoning, and eventual outcome."""

    context: dict[str, Any]
    options: list[str]
    selected_option: str
    rationale: dict[str, Any]
    outcome: str | None = None

    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
    )

    def to_dict(self):
        """Return the legacy dictionary representation used by demos and stores."""
        return self.model_dump(mode='python')

    def to_json_dict(self):
        """Return a JSON-friendly dictionary for API or persistence boundaries."""
        return self.model_dump(mode='json')
