import os
from typing import Optional

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from app.group.router import router as group_router
from app.model.error.error import Error
from app.model.error.error_handler import ErrorHandler
from app.user.router import router as user_router


class FastAPIApp(FastAPI):
    __description: str = """
It is a test user-group api for PostBeyond team. This api is created with help of FastAPI framework,
SqlAlchemy ORM and oriented to demonstrate wide range of FastAPI possibilities and developer's skills.

## Common errors
Api includes several error types which could happen in every flow.
So they won't be mentioned in every request description.
There are several groups of common errors: request format validation, internal and session
(it is based on user token which has expiration date,
so your requests will be blocked if you try to use expired session token etc).

- **400**: Request params have incorrect format
- **404**: Source not found
- **500**: Server error
"""
    __title: str = "PostBeyond"

    def __new__(cls) -> FastAPI:
        app: FastAPI = FastAPI.__new__(cls)
        app.__init__()
        app.description = cls.__description
        app.title = cls.__title

        versioned_app: FastAPI = VersionedFastAPI(app, enable_latest=True)

        versioned_app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

        cls.install_exception_handler(versioned_app)
        return versioned_app

    def __init__(self) -> None:
        super(FastAPIApp, self).__init__()

        self.include_router(group_router)
        self.include_router(user_router)

    @classmethod
    def install_exception_handler(cls, versioned_app: FastAPI) -> Optional:
        versioned_app.add_exception_handler(
            HTTPException,
            ErrorHandler.construct_handler(Error.not_found_error)
        )
        for sub_app in versioned_app.routes:
            if hasattr(sub_app.app, "add_exception_handler"):
                sub_app.app.add_exception_handler(
                    RequestValidationError,
                    ErrorHandler.validation
                )
                sub_app.app.add_exception_handler(ValueError, ErrorHandler.value)
                sub_app.app.add_exception_handler(
                    HTTPException,
                    ErrorHandler.construct_handler(Error.not_found_error)
                )
                sub_app.app.add_exception_handler(
                    Exception,
                    ErrorHandler.construct_handler(Error.internal_error)
                )
