from app.model.error.custom_error import CustomError


class Error:
    not_found_error: CustomError = CustomError(404, "Page not found")
    incorrect_params_format: CustomError = CustomError(400, 'Incorrect request data type or format')
    internal_error: CustomError = CustomError(500, "Internal server error")
