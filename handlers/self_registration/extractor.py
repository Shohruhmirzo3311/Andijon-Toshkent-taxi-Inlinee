from handlers.users.regexValidation import (NAME_RE, car_number_pattern,
                                            phone_pattern)



def normalize_text(text: str) -> str:
    return (
        text.replace("\n", " ")
            .replace("\t", " ")
            .replace("-", " ")
            .replace("  ", " ")
            .strip()
    )



def extract_name(text: str, fallback: str) -> str:
    m = NAME_RE.search(text)
    return m.group(2).strip() if m else fallback



def extract_phone(text: str, fallback: str = "") -> str:
    clean = text.replace(" ", "").replace("-", "")
    m = phone_pattern.search(text) or phone_pattern.search(clean)
    return m.group(0).strip() if m else fallback



def extract_car(text: str, fallback: str = "") -> str:
    m = car_number_pattern.search(text.upper())
    return m.group(0).strip() if m else fallback



