from typing import Callable, Optional
from http import HTTPStatus

from fastapi import APIRouter


class CustomApiRouter(APIRouter):

    def get(self, *args, **kwargs) -> Callable:
        return super(CustomApiRouter, self).get(
            *args,
            responses=self.get_responses_format(kwargs.get('status_code'), kwargs.get('responses')),
            **kwargs
        )

    def post(self, *args, **kwargs) -> Callable:
        return super(CustomApiRouter, self).post(
            *args,
            responses=self.get_responses_format(kwargs.get('status_code'), kwargs.get('responses')),
            **kwargs
        )

    def put(self, *args, **kwargs) -> Callable:
        return super(CustomApiRouter, self).put(
            *args,
            responses=self.get_responses_format(kwargs.get('status_code'), kwargs.get('responses')),
            **kwargs
        )

    def delete(self, *args, **kwargs) -> Callable:
        return super(CustomApiRouter, self).delete(
            *args,
            responses=self.get_responses_format(kwargs.get('status_code'), kwargs.get('responses')),
            **kwargs
        )

    def patch(self, *args, **kwargs) -> Callable:
        return super(CustomApiRouter, self).patch(
            *args,
            responses=self.get_responses_format(kwargs.get('status_code'), kwargs.get('responses')),
            **kwargs
        )

    @staticmethod
    def get_responses_format(status_code: Optional[int] = None, responses: Optional[dict] = None) -> dict:

        basic_model: dict = {
            "default": {
                "description": f"Possible response statuses are {status_code}"
                               f" and 420 if some exception happens"
            },
            420: {
                "content": {
                    "application/json": {
                        "example": {
                            "code": HTTPStatus.BAD_REQUEST,
                            "message": "Request params have incorrect format"
                        }
                    }
                },
                "description": "Unsuccessful response"
            }
        }

        if status_code == HTTPStatus.NO_CONTENT:
            basic_model.update({HTTPStatus.NO_CONTENT: {"description": "Empty successful response body"}})

        if status_code == HTTPStatus.CREATED:
            basic_model.update({HTTPStatus.CREATED: {"description": "Successfully created"}})

        if responses:
            basic_model = dict(basic_model, **responses)

        return basic_model
