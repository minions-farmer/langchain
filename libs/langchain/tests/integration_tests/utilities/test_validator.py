"""Integration test for Validator."""
from langchain.utilities.validator import ValidatorWrapper


def test_call() -> None:
    """Test that call runs."""
    twilio = ValidatorWrapper()
    output = twilio.run(
        params={
            "input_text": (
                "An apple is red. A banana is yellow. " "What color is an apple?"
            ),
            "generated_text": "An apple is red",
        }
    )
    assert output
