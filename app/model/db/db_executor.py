from fastapi_sqlalchemy import db

from app.model.error.error import Error


class DbExecutor:
    @classmethod
    def _commit(cls) -> None:
        try:
            db.session.commit()
        except Exception as e:
            cls.__handle_exception(e)

    @classmethod
    def _flush(cls) -> None:
        try:
            db.session.flush()
        except Exception as e:
            cls.__handle_exception(e)

    @staticmethod
    def __handle_exception(exception: Exception) -> None:
        try:
            print(exception)
            db.session.rollback()
        finally:
            raise Error.internal_error
