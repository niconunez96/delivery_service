from collections import namedtuple


Response = namedtuple("Response", ["body", "status_code"])

NOT_FOUND_RESPONSE = Response(
    {
        "error": "NOT_FOUND",
        "description": "Resource requested does not exist",
    },
    404,
)


def INVALID_RESPONSE(message: str) -> Response:
    return Response(
        {
            "error": "INVALID_REQUEST",
            "description": message,
        },
        400,
    )
