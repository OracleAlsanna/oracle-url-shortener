import random

from oracle.names import FROMSOFTWARE_NAMES


def pick_name(is_taken) -> str:
    """Return a random name from FROMSOFTWARE_NAMES not already in the database.

    is_taken: callable(name) -> bool
    Raises RuntimeError if all names are exhausted.
    """
    pool = FROMSOFTWARE_NAMES.copy()
    random.shuffle(pool)
    for name in pool:
        if not is_taken(name):
            return name
    raise RuntimeError("All FromSoftware names are taken. Delete some links to free up names.")
