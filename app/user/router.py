from http import HTTPStatus
from typing import List

from fastapi.responses import Response
from fastapi_versioning import version

from app.custom_api_router import CustomApiRouter
from app.user.fastapi.user_in.user_new_in import UserNewIn
from app.user.fastapi.user_out.user_out import UserOut
from app.user.user_data_processor import UserDataProcessor


router = CustomApiRouter(
    prefix="/users",
    tags=["User"]
)


@router.get("/", response_model=List[UserOut])
@version(0, 1)
def get_all_users() -> List[UserOut]:
    """
        ## Description
        Getting list of users

        ## Example

        **Response**
        ```
        [
            {
                "fullName": "Bill Underson",
                "status": "Active",
                "role": "User",
                "activeGroupNumber": 2,
                "groups": [
                    {
                        "name": "Dogs",
                        "status": "Active"
                    },
                    {
                        "name": "Kittens",
                        "status": "Active"
                    },
                    {
                        "name": "Birds",
                        "status": "Inactive"
                    }
                ]
            },
            {
                "fullName": "Walter Smith",
                "status": "Inactive",
                "role": "Admin",
                "activeGroupNumber": 1,
                "groups": [
                    {
                        "name": "Dogs",
                        "status": "Active"
                    },
                    {
                        "name": "Birds",
                        "status": "Inactive"
                    }
                ]
            }
        ]
        ```
    """
    return UserDataProcessor.get_all_users()


@router.post("/", status_code=HTTPStatus.CREATED)
@version(0, 1)
def create_user(user_new_in: UserNewIn, response: Response) -> Response:
    """
        ## Description
        Creation of new user

        ## Possible roles
        - **1** - user
        - **2** - admin

        ## Example

        **Request**
        ```
        {
            "firstName": "Bill",
            "lastName": "Underson",
            "email": "bill123@email.com",
            "roleId": 1,
            "groupId": 1
        }
        ```

        ## Possible error codes:
        - **602**: Group doesn't exist
        - **702**: User with the same email is already exist
    """
    return UserDataProcessor.create_user(user_new_in, response)


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
@version(0, 1)
def delete_user(user_id: int) -> Response:
    """
        ## Description
        Deletion of user

        ## Example

        **Request**

        ```
        /users/1
        ```
        *Deletion of user with id 1

        ## Possible error codes:
        - **704**: User doesn't exist
    """
    return UserDataProcessor.delete_user(user_id)


@router.put("/{user_id}/status/{status_id}", status_code=HTTPStatus.NO_CONTENT)
@version(0, 1)
def change_user_status(user_id: int, status_id: int) -> Response:
    """
        ## Description
        Changing user's status

        ## Possible statuses
        - **1** - active
        - **2** - inactive

        ## Example

        **Request url**
        ```
        /users/1/status/1
        ```
        *Activation of 1 group

        ## Possible error codes:
        - **704**: User doesn't exist
        - **1002**: Sent status is not exist
        - **1003**: New status is the same with the previous one
    """
    return UserDataProcessor.change_user_status(user_id, status_id)


@router.put("/{user_id}/groups/{group_id}", status_code=HTTPStatus.NO_CONTENT)
@version(0, 1)
def add_user_to_group(user_id: int, group_id: int) -> Response:
    """
        ## Description
        Adding user to the specific group

        ## Example

        **Request url**
        ```
        /users/1/groups/1
        ```
        *Adding user with id 1 to the group with id 1

        ## Possible error codes:
        - **602**: Group doesn't exist
        - **704**: User doesn't exist
        - **706**: User is already a member of the group
    """
    return UserDataProcessor.add_user_to_group(user_id, group_id)


@router.delete("/{user_id}/groups/{group_id}", status_code=HTTPStatus.NO_CONTENT)
@version(0, 1)
def delete_user_from_group(user_id: int, group_id: int) -> Response:
    """
        ## Description
        Deleting user from the specific group

        ## Example

        **Request url**
        ```
        /users/1/groups/1
        ```
        *Deleting user with id 1 from the group with id 1

        ## Possible error codes:
        - **602**: Group doesn't exist
        - **704**: User doesn't exist
        - **705**: User is not a member of the group
    """
    return UserDataProcessor.delete_user_from_group(user_id, group_id)
