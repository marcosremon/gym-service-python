from fastapi import APIRouter, Depends, Body
from starlette.responses import JSONResponse

from src.core.model.enums.role import Role
from src.service.configuration.dependency_injection import get_user_application
from src.transversal.request_response.user.create_admin.create_admin_request import CreateAdminRequest
from src.transversal.request_response.user.create_admin.create_admin_response import CreateAdminResponse
from src.transversal.request_response.user.create_generic_user.create_generic_user_request import CreateGenericUserRequest
from src.transversal.request_response.user.create_user.create_user_request import CreateUserRequest
from src.transversal.request_response.user.create_user.create_user_response import CreateUserResponse
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse

http = APIRouter(prefix="/api/user")

@http.get("/get-users", response_model = GetUsersResponse)
async def get_users(application = Depends(get_user_application)):
    try:
        get_users_response = await application.get_users()
        if get_users_response.is_success:
            return JSONResponse(
                content = get_users_response.dict(),
                status_code = get_users_response.response_codes_json
            )

        return JSONResponse(
            content = get_users_response.dict(),
            status_code = get_users_response.response_codes_json
        )
    except Exception as e:
        error_response = GetUsersResponse(
                is_success = False,
                message = str(f"unexpected error in get-users controller -->: {e}"),
                response_codes_json = 500,
                users=[]
        ),

        return JSONResponse(
            content = error_response.dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/create-user", response_model = CreateUserResponse)
async def create_user(create_user: CreateUserRequest = Body(), application = Depends(get_user_application)):
    try:
        generic_user_request = CreateGenericUserRequest(
            dni = create_user.dni,
            username = create_user.username,
            surname = create_user.surname,
            email = create_user.email,
            password = create_user.password,
            confirm_password = create_user.confirm_password,
            role = Role.USER
        )

        create_user_response = await application.create_user(generic_user_request)
        if create_user_response.is_success:
            return JSONResponse(
                content = create_user_response.dict(),
                status_code = create_user_response.response_codes_json
            )

        return JSONResponse(
            content = create_user_response.dict(),
            status_code = create_user_response.response_codes_json
        )
    except Exception as e:
        error_response = CreateUserResponse(
            is_success = False,
            message = str(f"unexpected error in create-user controller -->: {e}"),
            response_codes_json = 500,
        )

        return JSONResponse(
            content = error_response.dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/create-admin", response_model = CreateAdminResponse)
async def create_user(create_admin: CreateAdminRequest, application = Depends(get_user_application)):
    try:
        generic_admin_request = CreateGenericUserRequest(
            dni = create_admin.dni,
            username = create_admin.username,
            surname = create_admin.surname,
            email = create_admin.email,
            password = create_admin.password,
            confirm_password = create_admin.confirm_password,
            role = Role.ADMIN
        )

        create_admin_response = await application.create_user(generic_admin_request)
        if create_admin_response.is_success:
            return JSONResponse(
                content = create_admin_response.dict(),
                status_code = create_admin_response.response_codes_json
            )

        return JSONResponse(
            content = create_admin_response.dict(),
            status_code = create_admin_response.response_codes_json
        )
    except Exception as e:
        error_response = CreateAdminResponse(
            is_success = False,
            message = str(f"unexpected error in create-admin controller -->: {e}"),
            response_codes_json = 500,
        )

        return JSONResponse(
            content = error_response.dict(),
            status_code = error_response.response_codes_json
        )