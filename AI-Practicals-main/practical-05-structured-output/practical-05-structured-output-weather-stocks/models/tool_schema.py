from pydantic import BaseModel, Field


class ToolDecision(BaseModel):
    tool: str = Field(
        description="Selected tool name"
    )

    input: str = Field(
        description="Input for the selected tool"
    )