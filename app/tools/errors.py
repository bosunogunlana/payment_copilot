from pydantic import BaseModel, Field


class ToolError(BaseModel):
    code: str
    retryable: bool = False
    message: str = Field(min_length=1)

    @staticmethod
    def error_code_to_message(code: str) -> str:
        return {
            "UNAUTHORIZED": "Access denied",
            "INVALID_ARGUMENTS": "invalid Argument",
            "UNKNOWN_TOOL": "Unknown Tool",
        }.get(code, "")
