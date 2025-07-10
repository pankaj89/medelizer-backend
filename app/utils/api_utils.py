from fastapi.responses import JSONResponse
from starlette import status


def success_response(msg, data=None):
    print("data:", data)
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
