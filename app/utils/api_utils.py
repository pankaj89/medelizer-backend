from fastapi.responses import JSONResponse
from starlette import status


def success_response(msg, data=None):
    """
    Returns a JSON response indicating success with a message and optional data.

    Args:
        msg (str): The success message to return.
        data (dict, optional): Additional data to include in the response.

    Returns:
        JSONResponse: A JSON response with HTTP status 200.
    """
    if data is not None:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": msg, 'data': data}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": msg}
        )


def error_response(msg, data):
    """
    Returns a JSON response indicating error with a message and optional data.

    Args:
        msg (str): The success message to return.
        data (dict, optional): Additional data to include in the response.

    Returns:
        JSONResponse: A JSON response with HTTP status 400.
    """
    if data is not None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": msg, 'data': data}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": msg}
        )
