"""Basic/shared functionality for the Business Logic Layer.

"""

from pydantic import BaseModel, ValidationError


def gen_clean_data(data: list[dict], model: BaseModel) -> list[dict]:
    cleaned_data = []
    for entry in data:
        try:
            cleaned_entry = model(entry).dict()
        except ValidationError:
            continue
        cleaned_data.append(cleaned_entry)
    return cleaned_data
