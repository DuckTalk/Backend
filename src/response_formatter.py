def format(response: dict|str|None) -> dict:
    if response is None:
        response = "Unknown internal error, please contact a maintainer"

    return {
        "error": not isinstance(response, dict),
        "data": response
    }
