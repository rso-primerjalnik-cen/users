from starlette import status
from typing import Any, Optional, Dict

from fastapi import HTTPException


class AttrValidationHTTPException(HTTPException):
    """
    detail / error message structure follows error structure that Pydantic models return on validation errors
    """
    def __init__(self, status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY, attr: str = None,
                 attr_error: str = None, detail: Any = None, headers: Optional[Dict[str, Any]] = None) -> None:
        if attr and attr_error:
            detail_content = dict(loc=['body', attr],
                                  msg=attr_error,
                                  type='invalid_value')
            detail = f'[{json.dumps(detail_content)}]'
        super().__init__(status_code, detail, headers)
