from http import HTTPStatus
from typing import List

from fastapi_versioning import version
from fastapi.responses import Response

from app.custom_api_router import CustomApiRouter
from app.group.fastapi.group_in.group_edit_in import GroupEditIn
from app.group.fastapi.group_in.group_new_in import GroupNewIn
from app.group.fastapi.group_out.detailed_group_out import DetailedGroupOut
from app.group.group_data_processor import GroupDataProcessor


router = CustomApiRouter(
    prefix="/groups",
    tags=["Group"]
)


@router.post("/", status_code=HTTPStatus.CREATED)
@version(0, 1)
def create_group(group_new_in: GroupNewIn, response: Response) -> Response:
    """
        ## Description
        Creation of new group

        ## Example

        **Request**
        ```
        {
            "name": "Funny activities"
        }
        ```

        ## Possible error codes:
        - **601**: Group with the same name is already exist
    """
    return GroupDataProcessor.create_group(group_new_in, response)


@router.patch("/{group_id}", status_code=HTTPStatus.NO_CONTENT)
@version(0, 1)
def edit_group(group_id: int, group_in: GroupEditIn) -> Response:
    """
        ## Description
        Editing group's name

        ## Example

        **Request**
        ```
        {
            "name": "Funny activities and stories", //Optional field
        }
        ```

        ## Possible error codes:
        - **601**: Group with the same name is already exist
        - **602**: Group doesn't exist
        - **603**: New group name is the same with the previous one"
        - **1001**: Nothing has been changed
    """
    return GroupDataProcessor.edit_group(group_id, group_in)


@router.put("/{group_id}/status/{status_id}", status_code=HTTPStatus.NO_CONTENT)
@version(0, 1)
def edit_group(group_id: int, status_id: int) -> Response:
    """
        ## Description
        Changing group's status

        ## Possible statuses
        - **1** - active
        - **2** - inactive

        ## Example

        **Request url**
        ```
        /groups/1/status/1
        ```
        *Activation of 1 group

        ## Possible error codes:
        - **602**: Group doesn't exist
        - **1002**: Sent status does not exist
        - **1003**: New status is the same with the previous one
    """
    return GroupDataProcessor.change_group_status(group_id, status_id)


@router.get("/", response_model=List[DetailedGroupOut])
@version(0, 1)
def get_all_groups() -> List[DetailedGroupOut]:
    """
        ## Description
        Getting list of groups

        ## Example

        **Response**
        ```
        [
            {
                "name": "Dogs",
                "status": "Active",
                "users": [
                    {
                        "fullName": "John Tak",
                        "resourceUri": "/users/2"
                    },
                    {
                        "fullName": "Yan Green",
                        "resourceUri": "/users/3"
                    }
                ]
            },
            {
                "name": "Birds",
                "status": "Inactive",
                "users": [
                    {
                        "fullName": "Donald Duck",
                        "resourceUri": "/users/1"
                    },
                    {
                        "fullName": "John Tak",
                        "resourceUri": "/users/2"
                    }
                ]
            }
        ]
        ```
    """
    return GroupDataProcessor.get_all_groups()
