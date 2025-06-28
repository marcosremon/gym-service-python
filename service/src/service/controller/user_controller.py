from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from src.core.model.enums.role import Role
from src.infraestructure.dependency.dependency_injection import get_user_application
from src.transversal.common.response_codes_json import ResponseCodesJson
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

@http.get("/get-users", response_model = GetUsersResponse)
async def get_users(application = Depends(get_user_application)):
    try:
        get_users_response = await application.get_users()
        if get_users_response.is_success:
            json_response = JSONResponse(
                status_code = get_users_response.response_codes_json,
                content = GetUsersResponse(
                    response_codes_json = get_users_response.response_codes_json,
                    is_success = get_users_response.is_success,
                    message = get_users_response.message,
                    users = get_users_response.users,
                )
            )
        else:
            json_response = JSONResponse(
                status_code = get_users_response.response_codes_json,
                content = GetUsersResponse(
                    response_codes_json = get_users_response.response_codes_json,
                    is_success = get_users_response.is_success,
                    message = get_users_response.message,
                    users = get_users_response.users,
                )
            )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = GetUsersResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on get_users controller: {e}"),
            )
        )

    return json_response

@http.post("/get-user-by-email", response_model = GetUserByEmailResponse)
async def get_user_by_email(get_user_by_email_request:  GetUserByEmailRequest, application = Depends(get_user_application)):
    try:
        if get_user_by_email.email is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = GetUserByEmailResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str("invalid data, the inputs parameters are null or empty"),
                )
            )
        else:
            get_user_by_email_response = await application.get_user_by_email(get_user_by_email_request)
            if get_user_by_email_response.is_success:
                json_response = JSONResponse(
                    status_code = get_user_by_email_response.response_codes_json,
                    content = GetUserByEmailResponse(
                        response_codes_json = get_user_by_email_response.response_codes_json,
                        is_success = get_user_by_email_response.is_success,
                        message = get_user_by_email_response.message,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = get_user_by_email_response.response_codes_json,
                    content = GetUserByEmailResponse(
                        response_codes_json = get_user_by_email_response.response_codes_json,
                        is_success = get_user_by_email_response.is_success,
                        message = get_user_by_email_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = GetUserByEmailResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on get_user_by_email controller: {e}"),
            )
        )

    return json_response

@http.post("/create-user", response_model = CreateUserResponse)
async def create_user(create_user_request: CreateUserRequest, application = Depends(get_user_application)):
    try:
        if (create_user_request.email is None
                or create_user_request.dni is None
                or create_user_request.username is None
                or create_user_request.password is None
                or create_user_request.confirm_password is None):
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = CreateUserResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, the inputs parameters are null or empty"),
                ).dict()
            )
        else:
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
                json_response = JSONResponse(
                    status_code = create_user_response.response_codes_json,
                    content = CreateUserResponse(
                        response_codes_json = create_user_response.response_codes_json,
                        is_success = create_user_response.is_success,
                        message = create_user_response.message,
                        user_dto = create_user_response.user_dto,
                    ).dict()
                )
            else:
                json_response = JSONResponse(
                    status_code = create_user_response.response_codes_json,
                    content = CreateUserResponse(
                        response_codes_json = create_user_response.response_codes_json,
                        is_success = create_user_response.is_success,
                        message = create_user_response.message,
                    ).dict()
                )
    except Exception as ex:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = CreateUserResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on create_user controller: {ex}"),
            ).dict()
        )

    return json_response

@http.post("/create-google-user", response_model = CreateGoogleUserResponse)
async def create_google_user(create_google_user_request: CreateGoogleUserRequest, application = Depends(get_user_application)):
    try:
        if create_google_user_request.email is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = CreateGoogleUserResponse(
                    response_codes_json=ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, the inputs parameters are null or empty"),
                )
            )
        else:
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
                json_response = JSONResponse(
                    status_code = create_google_user_response.response_codes_json,
                    content = CreateGoogleUserResponse(
                        response_codes_json = create_google_user_response.response_codes_json,
                        is_success = create_google_user_response.is_success,
                        message = create_google_user_response.message,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = create_google_user_response.response_codes_json,
                    content = CreateGoogleUserResponse(
                        response_codes_json = create_google_user_response.response_codes_json,
                        is_success = create_google_user_response.is_success,
                        message = create_google_user_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = CreateGoogleUserResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on create_google_user controller: {e}"),
            )
        )

    return json_response

@http.post("/create-admin", response_model = CreateAdminResponse)
async def create_admin(create_admin_request: CreateAdminRequest, application = Depends(get_user_application)):
    try:
        if (create_admin_request.email is None
                or create_admin_request.dni is None
                or create_admin_request.username is None
                or create_admin_request.password is None
                or create_admin_request.confirm_password is None):
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = CreateAdminResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, the inputs parameters are null or empty"),
                ).dict()
            )
        else:
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
                json_response = JSONResponse(
                    status_code = create_admin_response.response_codes_json,
                    content = CreateAdminResponse(
                        response_codes_json = create_admin_response.response_codes_json,
                        is_success = create_admin_response.is_success,
                        message = create_admin_response.message,
                    ).dict()
                )
            else:
                json_response = JSONResponse(
                    status_code = create_admin_response.response_codes_json,
                    content = CreateAdminResponse(
                        response_codes_json = create_admin_response.response_codes_json,
                        is_success = create_admin_response.is_success,
                        message = create_admin_response.message,
                    ).dict()
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = CreateAdminResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on create_admin_user controller: {e}"),
            ).dict()
        )

    return json_response

@http.post("/update-user", response_model = UpdateUserResponse)
async def update_user(update_user_request: UpdateUserRequest, application = Depends(get_user_application)):
    try:
        if update_user_request.email is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = UpdateUserResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, the inputs parameters are null or empty"),
                )
            )
        else:
            update_user_response = await application.update_user(update_user_request)
            if update_user_response.is_success:
                json_response = JSONResponse(
                    status_code = update_user_response.response_codes_json,
                    content = UpdateUserResponse(
                        response_codes_json = update_user_response.response_codes_json,
                        is_success = update_user_response.is_success,
                        message = update_user_response.message,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = update_user_response.response_codes_json,
                    content = UpdateUserResponse(
                        response_codes_json = update_user_response.response_codes_json,
                        is_success = update_user_response.is_success,
                        message = update_user_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = UpdateUserResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on update_user controller: {e}"),
            )
        )

    return json_response

@http.post("/delete-user", response_model = DeleteUserResponse)
async def delete_user(delete_user_request: DeleteUserRequest, application = Depends(get_user_application)):
    try:
        if delete_user_request.email is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = DeleteUserResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, the inputs parameters are null or empty"),
                )
            )
        else:
            delete_user_response = await application.delete_user(delete_user_request)
            if delete_user_response.is_success:
                json_response = JSONResponse(
                    status_code = delete_user_response.response_codes_json,
                    content = DeleteUserResponse(
                        response_codes_json = delete_user_response.response_codes_json,
                        is_success = delete_user_response.is_success,
                        message = delete_user_response.message,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = delete_user_response.response_codes_json,
                    content=DeleteUserResponse(
                        response_codes_json = delete_user_response.response_codes_json,
                        is_success = delete_user_response.is_success,
                        message = delete_user_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = DeleteUserResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on delete_user controller: {e}"),
            )
        )

    return json_response

@http.post("/create-new-password", response_model = CreateNewPasswordResponse)
async def create_new_password(create_new_password_request: CreateNewPasswordRequest, application = Depends(get_user_application)):
    try:
        if create_new_password_request.email is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = CreateNewPasswordResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, the inputs parameters are null or empty"),
                )
            )
        else:
            create_new_password_response = await application.create_new_password(create_new_password_request)
            if create_new_password_response.is_success:
                json_response = JSONResponse(
                    status_code = create_new_password_response.response_codes_json,
                    content = CreateNewPasswordResponse(
                        response_codes_json = create_new_password_response.response_codes_json,
                        is_success = create_new_password_response.is_success,
                        message = create_new_password_response.message,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = create_new_password_response.response_codes_json,
                    content = CreateNewPasswordResponse(
                        response_codes_json = create_new_password_response.response_codes_json,
                        is_success = create_new_password_response.is_success,
                        message = create_new_password_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = CreateNewPasswordResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on create_new_password controller: {e}"),
            )
        )

    return json_response

@http.post("/create-new-password-with-email-and-password", response_model = CreateNewPasswordWithEmailAndPasswordResponse)
async def create_new_password(create_new_password_request: CreateNewPasswordWithEmailAndPasswordRequest, application = Depends(get_user_application)):
    try:
        if create_new_password_request.email is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = CreateNewPasswordWithEmailAndPasswordResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, the inputs parameters are null or empty"),
                )
            )
        else:
            create_new_password_response = await application.create_new_password_with_email_and_password(
                create_new_password_request)
            if create_new_password_response.is_success:
                json_response = JSONResponse(
                    status_code = create_new_password_response.response_codes_json,
                    content = CreateNewPasswordWithEmailAndPasswordResponse(
                        response_codes_json = create_new_password_response.response_codes_json,
                        is_success = create_new_password_response.is_success,
                        message = create_new_password_response.message,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = create_new_password_response.response_codes_json,
                    content = CreateNewPasswordWithEmailAndPasswordResponse(
                        response_codes_json = create_new_password_response.response_codes_json,
                        is_success = create_new_password_response.is_success,
                        message = create_new_password_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = CreateNewPasswordWithEmailAndPasswordResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on create_new_password controller: {e}"),
            )
        )

    return json_response