from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from src.core.model.enums.role import Role
from src.service.configuration.dependency_injection import get_user_application
from src.transversal.request_response.user.create_admin.create_admin_request import CreateAdminRequest
from src.transversal.request_response.user.create_admin.create_admin_response import CreateAdminResponse
from src.transversal.request_response.user.create_generic_user.create_generic_user_request import CreateGenericUserRequest
from src.transversal.request_response.user.create_google_user.create_google_user_request import CreateGoogleUserRequest
from src.transversal.request_response.user.create_google_user.create_google_user_response import CreateGoogleUserResponse
from src.transversal.request_response.user.create_new_password.create_new_password_request import CreateNewPasswordRequest
from src.transversal.request_response.user.create_new_password.create_new_password_response import CreateNewPasswordResponse
from src.transversal.request_response.user.create_new_password_with_email_and_password.create_new_password_with_email_and_password_request import CreateNewPasswordWithEmailAndPasswordRequest
from src.transversal.request_response.user.create_new_password_with_email_and_password.create_new_password_with_email_and_password_response import CreateNewPasswordWithEmailAndPasswordResponse
from src.transversal.request_response.user.create_user.create_user_request import CreateUserRequest
from src.transversal.request_response.user.create_user.create_user_response import CreateUserResponse
from src.transversal.request_response.user.delete_user.delete_user_request import DeleteUserRequest
from src.transversal.request_response.user.delete_user.delete_user_response import DeleteUserResponse
from src.transversal.request_response.user.get_user_by_email.get_user_by_email_request import GetUserByEmailRequest
from src.transversal.request_response.user.get_user_by_email.get_user_by_email_response import GetUserByEmailResponse
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse
from src.transversal.request_response.user.update_user.update_user_request import UpdateUserRequest
from src.transversal.request_response.user.update_user.update_user_response import UpdateUserResponse

http = APIRouter(prefix="/api/user")

@http.post("/create-user", response_model = CreateUserResponse)
async def create_user(create_user_request: CreateUserRequest, application = Depends(get_user_application)):
    try:
        generic_user_request = CreateGenericUserRequest(
            dni = create_user_request.dni,
            username = create_user_request.username,
            surname = create_user_request.surname,
            email = create_user_request.email,
            password = create_user_request.password,
            confirm_password = create_user_request.confirm_password,
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
            status_code=error_response.response_codes_json
        )

@http.post("/get-user-by-email", response_model = GetUserByEmailResponse)
async def get_user_by_email(get_user_by_email_request:  GetUserByEmailRequest, application = Depends(get_user_application)):
    try:
        get_user_by_email_response = await application.get_user_by_email(get_user_by_email_request)
        if get_user_by_email_response.is_success:
            return JSONResponse(
                content = get_user_by_email_response.dict(),
                status_code = get_user_by_email_response.response_codes_json
            )

        return JSONResponse(
            content = get_user_by_email_response.dict(),
            status_code = get_user_by_email_response.response_codes_json
        )
    except Exception as e:
        error_response = GetUserByEmailResponse(
            is_success = False,
            message = str(f"unexpected error in get-user-by-email controller -->: {e}"),
            response_codes_json = 500,
        )

        return JSONResponse(
            content = error_response.dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/create-google-user", response_model = CreateGoogleUserResponse)
async def create_user(create_google_user_request: CreateGoogleUserRequest, application = Depends(get_user_application)):
    try:
        generic_google_user_request = CreateGenericUserRequest(
            dni = create_google_user_request.dni,
            username = create_google_user_request.username,
            surname = create_google_user_request.surname,
            email = create_google_user_request.email,
            password = create_google_user_request.email,
            confirm_password = create_google_user_request.confirm_password,
            role = Role.USER
        )

        create_google_user_response = await application.create_google_user(generic_google_user_request)
        if create_google_user_response.is_success:
            return JSONResponse(
                content = create_google_user_response.dict(),
                status_code = create_google_user_response.response_codes_json
            )

        return JSONResponse(
            content = create_google_user_response.dict(),
            status_code = create_google_user_response.response_codes_json
        )
    except Exception as e:
        error_response = CreateGoogleUserResponse(
            is_success = False,
            message = str(f"unexpected error in create-google-user controller -->: {e}"),
            response_codes_json = 500,
        )

        return JSONResponse(
            content = error_response.dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/create-admin", response_model = CreateAdminResponse)
async def create_user(create_admin_request: CreateAdminRequest, application = Depends(get_user_application)):
    try:
        generic_admin_request = CreateGenericUserRequest(
            dni = create_admin_request.dni,
            username = create_admin_request.username,
            surname = create_admin_request.surname,
            email = create_admin_request.email,
            password = create_admin_request.password,
            confirm_password = create_admin_request.confirm_password,
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

@http.post("/update-user", response_model = UpdateUserResponse)
async def update_user(update_user_request: UpdateUserRequest, application = Depends(get_user_application)):
    try:
        update_user_response = await application.update_user(update_user_request)
        if update_user_response.is_success:
            return JSONResponse(
                content = update_user_response.dict(),
                status_code = update_user_response.response_codes_json
            )

        return JSONResponse(
            content = update_user_response.dict(),
            status_code = update_user_response.response_codes_json
        )
    except Exception as e:
        error_response = UpdateUserResponse(
            is_success = False,
            message = str(f"unexpected error in update-user controller -->: {e}"),
            response_codes_json = 500,
        )

        return JSONResponse(
            content = error_response.dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/delete-user", response_model = DeleteUserResponse)
async def delete_user(delete_user_request: DeleteUserRequest, application = Depends(get_user_application)):
    try:
        delete_user_response = await application.delete_user(delete_user_request)
        if delete_user_response.is_success:
            return JSONResponse(
                content = delete_user_response.dict(),
                status_code = delete_user_response.response_codes_json
            )

        return JSONResponse(
            content = delete_user_response.dict(),
            status_code = delete_user_response.response_codes_json
        )
    except Exception as e:
        error_response = DeleteUserResponse(
            is_success = False,
            message = str(f"unexpected error in delete-user controller -->: {e}"),
            response_codes_json = 500,
        )

        return JSONResponse(
            content = error_response.dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/create-new-password", response_model = CreateNewPasswordResponse)
async def create_new_password(create_new_password_request: CreateNewPasswordRequest, application = Depends(get_user_application)):
    try:
        create_new_password_response = await application.create_new_password(create_new_password_request)
        if create_new_password_response.is_success:
            return JSONResponse(
                content = create_new_password_response.dict(),
                status_code = create_new_password_response.response_codes_json
            )

        return JSONResponse(
            content = create_new_password_response.dict(),
            status_code = create_new_password_response.response_codes_json
        )
    except Exception as e:
        error_response = CreateNewPasswordResponse(
            is_success = False,
            message = f"unexpected error in create-new-password controller -->: {e}",
            response_codes_json = 500,
        )

        return JSONResponse(
            content = error_response.dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/create-new-password-with-email-and-password", response_model = CreateNewPasswordWithEmailAndPasswordResponse)
async def create_new_password(create_new_password_request: CreateNewPasswordWithEmailAndPasswordRequest, application = Depends(get_user_application)):
    try:
        create_new_password_response = await application.create_new_password_with_email_and_password(create_new_password_request)
        if create_new_password_response.is_success:
            return JSONResponse(
                content = create_new_password_response.dict(),
                status_code = create_new_password_response.response_codes_json
            )

        return JSONResponse(
            content = create_new_password_response.dict(),
            status_code = create_new_password_response.response_codes_json
        )
    except Exception as e:
        error_response = CreateNewPasswordResponse(
            is_success = False,
            message = f"unexpected error in create-new-password-with-email-and-password controller -->: {e}",
            response_codes_json = 500,
        )

        return JSONResponse(
            content = error_response.dict(),
            status_code = error_response.response_codes_json
        )