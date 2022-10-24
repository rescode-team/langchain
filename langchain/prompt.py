"""Prompt schema definition."""
from typing import Any, Dict, List

from pydantic import BaseModel, Extra, root_validator

from langchain.formatting import formatter

_FORMATTER_MAPPING = {
    "f-string": formatter.format,
}


class Prompt(BaseModel):
    """Schema to represent a prompt for an LLM."""

    input_variables: List[str]
    template: str
    template_format: str = "f-string"

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def format(self, **kwargs: Any) -> str:
        """Format the prompt with the inputs."""
        return _FORMATTER_MAPPING[self.template_format](self.template, **kwargs)

    @root_validator()
    def template_is_valid(cls, values: Dict) -> Dict:
        """Check that template and input variables are consistent."""
        input_variables = values["input_variables"]
        template = values["template"]
        template_format = values["template_format"]
        if template_format not in _FORMATTER_MAPPING:
            valid_formats = list(_FORMATTER_MAPPING)
            raise ValueError(
                f"Invalid template format. Got `{template_format}`;"
                f" should be one of {valid_formats}"
            )
        dummy_inputs = {input_variable: "foo" for input_variable in input_variables}
        try:
            formatter_func = _FORMATTER_MAPPING[template_format]
            formatter_func(template, **dummy_inputs)
        except KeyError:
            raise ValueError("Invalid prompt schema.")
        return values
