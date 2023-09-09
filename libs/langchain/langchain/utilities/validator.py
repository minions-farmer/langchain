import logging
from typing import Any, Dict, Optional

import requests

from langchain.pydantic_v1 import BaseModel, root_validator
from langchain.utils import get_from_dict_or_env

logger = logging.getLogger(__name__)
_NAME = "Validator"
_URL = "https://validator.minions.farm"


class ValidatorWrapper(BaseModel):
    """
    Wrapper around Validator API.

    Parameters:
    TODO
    """

    parse: Any  #: :meta private:
    validator_api_key: Optional[str] = None

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["validator_api_key"] = get_from_dict_or_env(
            values, "validator_api_key", f"{_NAME.upper()}_API_KEY"
        )
        return values

    def run(self, params: Dict[str, str]) -> str:
        """
        TODO
        """

        try:
            headers = {"Authorization": f"Bearer {self.validator_api_key}"}
            r = requests.post(f"{_URL}/api/annotate", headers=headers, json=params)
            if r.status_code == 200:
                return f"{_URL}/api/annotations?doc_id={r.json()['doc_id']}"
            elif r.status_code == 403:
                return f"{_NAME} permission error"
            else:
                return f"{_NAME} error {r.text}"
        except Exception as ex:
            return f"{_NAME} exception: {ex}"
