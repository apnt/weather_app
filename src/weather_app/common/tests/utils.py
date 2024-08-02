import random
import string


def get_auth_header(access_token: str):
    return {"Authorization": f"Bearer {access_token}"}


def get_random_string(
    length: int = 32,
    use_lowercase: bool = True,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_punctuation: bool = True,
):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation

    chars_to_use = ""
    chars_to_use += lowercase if use_lowercase else ""
    chars_to_use += uppercase if use_uppercase else ""
    chars_to_use += digits if use_digits else ""
    chars_to_use += punctuation if use_punctuation else ""

    chars = list(chars_to_use)
    random.shuffle(chars)
    return "".join(random.choices(chars, k=length))
