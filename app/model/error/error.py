from app.model.error.custom_error import CustomError


class Error:
    not_found_error: CustomError = CustomError(404, "Page not found")
    incorrect_params_format: CustomError = CustomError(400, 'Incorrect request data type or format')
    internal_error: CustomError = CustomError(500, "Internal server error")

    group_already_exist: CustomError = CustomError(601, "Group with the same name is already exist")
    group_not_exist: CustomError = CustomError(602, "Group doesn't exist")
    group_name_is_the_same: CustomError = CustomError(603, "New group name is the same with the previous one")

    invalid_email_format: CustomError = CustomError(701, "Invalid email format")
    user_with_same_email_exist: CustomError = CustomError(702, "User with the same email is already exist")
    role_not_exist: CustomError = CustomError(703, "User role doesn't exist")
    user_not_exist: CustomError = CustomError(704, "User doesn't exist")
    user_is_not_member: CustomError = CustomError(705, "User is not a member of the group")
    user_is_member: CustomError = CustomError(706, "User is already a member of the group")

    nothing_changed: CustomError = CustomError(1001, "Nothing has been changed")
    status_not_exist: CustomError = CustomError(1002, "Sent status is not exist")
    status_is_the_same: CustomError = CustomError(1003, "New status is the same with the previous one")
