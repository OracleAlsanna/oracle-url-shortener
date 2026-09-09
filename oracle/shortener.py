import random
import re
import string

GENERATED_CODES = list(string.ascii_uppercase + string.digits)

CUSTOM_CODE_PATTERN = re.compile(r"^[A-Za-z0-9]{3,20}$")


def generate_code(is_taken) -> str:
    for _ in range(10000):
        code = "".join(random.choices(GENERATED_CODES, k=4))
        if not is_taken(code):
            return code
    raise RuntimeError(
        "Could not generate a unique code. Delete some links to free up codes."
    )


def validate_custom_code(code: str) -> None:
    """Raise ValueError if a user-supplied custom code is not a valid format."""
    if not CUSTOM_CODE_PATTERN.match(code):
        raise ValueError(
            "Custom codes must be 3-20 characters, letters and digits only."
        )
