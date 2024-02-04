from pydantic import validate_call
from typing import Union

VALIDATE_CONFIG = dict(arbitrary_types_allowed = True)

@validate_call(config = VALIDATE_CONFIG)
def compare_dicts(dict1: dict, dict2: dict) -> bool:
    if set(dict1.keys()) != set(dict2.keys()):
        return False
    
    for key in dict1:
        if dict1[key] != dict2[key]:
            return False

    return True

@validate_call(config = VALIDATE_CONFIG)
def read_file(file_path: str, encoding: str = "utf-8") -> str:
    with open(file_path, encoding = encoding) as file:
        content = file.read()

    return content

@validate_call(config = VALIDATE_CONFIG)
def convert_value(value: str) -> Union[str, int, float, bool, None]:
    for converter in (int, float, to_bool):
        try:
            return converter(value)
        except ValueError:
            pass
    return value

@validate_call(config = VALIDATE_CONFIG)
def to_bool(value: str) -> bool:
    value = value.lower().strip()
    if value in [ "true", "false" ]:
        return value.lower() == "true"

    raise ValueError(f"Invalid boolean value '{value}'")

@validate_call(config = VALIDATE_CONFIG)
def parse_list(value: str) -> list[Union[str, int, float, bool, None]]:
    elements = value[1:-1].split(",")
    return [ convert_value(elem.strip()) for elem in elements ]

@validate_call(config = VALIDATE_CONFIG)
def parse_tuple(value: str) -> tuple[Union[str, int, float, bool, None]]:
    elements = value[1:-1].split(",")
    return tuple(convert_value(elem.strip()) for elem in elements)