from typing import Callable, Optional

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
                "description": f"Possible response statuses are {204 if status_code == 204 else 200}"
                               f" and 420 if some exception happens"
            },
            420: {
                "content": {
                    "application/json": {
                        "example": {
                            "code": 400,
                            "message": "Request params have incorrect format"
                        }
                    }
                },
                "description": "Unsuccessful response"
            }
        }

        if status_code == 204:
            basic_model.update({204: {"description": "Empty successful response body"}})

        if responses:
            basic_model = dict(basic_model, **responses)

        return basic_model
