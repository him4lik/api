def pin_validator(value):
    if len(value) != 6 or not value[:].isdigit():
        return False

    return True