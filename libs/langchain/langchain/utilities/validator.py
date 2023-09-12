import logging
from typing import Any, Dict, List, Optional

import requests

from langchain.pydantic_v1 import BaseModel, root_validator
from langchain.utils import get_from_dict_or_env

logger = logging.getLogger(__name__)
_NAME = "Validator"
_URL = "https://validator.minions.farm"


class ValidatorWrapper(BaseModel):
    """Wrapper for visually validating an LLM prompt and its output

    To use this wrapper, set the env variable ``VALIDATOR_API_KEY`` or pass
    ``validator_api_key`` as named parameter to the constructor. Get your api key from
    https://validator.minions.farm/settings

    Example:
        .. code-block:: python

            from langchain.utilities.validator import ValidatorWrapper
            validator = ValidatorWrapper()
            validator.run(
                generated_text="An apple is red",
                input_text="An apple is red. A banana is yellow. What color is an apple"
            )
    """

    parse: Any  #: :meta private:
    """Validator api key"""
    validator_api_key: Optional[str] = None

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["validator_api_key"] = get_from_dict_or_env(
            values, "validator_api_key", f"{_NAME.upper()}_API_KEY"
        )
        return values

    def run(
        self, input_text: str, generated_text: str, checklist: Optional[List[str]] = []
    ) -> str:
        """
        Args:
            input_text: The original text that serves as input to a language model like
                GPT.
            generated_text: The text output produced by the language model in response
                to the input text. This could be an answer, explanation, or any other
                form of textual content.
            checklist: An array containing guidelines or criteria that the language
                model's output should ideally meet. These guidelines may not have been
                directly provided to the model but serve as post-hoc checks.
        Returns:
            str: A URL pointing to a webpage that visualizes the language model's output
                based on the given input text and guidelines.
        """

        try:
            headers = {"Authorization": f"Bearer {self.validator_api_key}"}
            payload = {
                "input_text": input_text,
                "generated_text": generated_text,
            }
            if checklist:
                payload["checklist"] = checklist
            r = requests.post(f"{_URL}/api/annotate", headers=headers, json=payload)
            if r.status_code == 200:
                return f"{_URL}/api/annotations?doc_id={r.json()['doc_id']}"
            elif r.status_code == 403:
                return f"{_NAME} permission error"
            else:
                return f"{_NAME} error {r.text}"
        except Exception as ex:
            return f"{_NAME} exception: {ex}"
