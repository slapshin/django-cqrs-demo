import dataclasses

from apps.core.logic.errors import InvalidInputApplicationError
from apps.core.utils.objects import empty


def validate_input(input_data, validator_class) -> dict[str, object]:
    """
    Validate input data.

    Raise exception if data is invalid.
    """
    to_validate = {
        data_key: data_value
        for data_key, data_value in dataclasses.asdict(input_data).items()
        if data_value != empty
    }

    validator = validator_class(data=to_validate)
    if not validator.is_valid():
        raise InvalidInputApplicationError(validator.errors)

    return validator.validated_data
