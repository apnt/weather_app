from rest_framework import exceptions as drf_exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):

    # 400 bad request response
    if isinstance(exc, drf_exceptions.ValidationError):
        error_response = {"message": "Invalid request data.", "details": exc.detail}
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    # 401 unauthenticated responses
    if isinstance(exc, drf_exceptions.AuthenticationFailed):
        error_response = {"message": "Invalid credentials."}
        return Response(error_response, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, drf_exceptions.NotAuthenticated):
        error_response = {"message": "Authentication credentials were not provided."}
        return Response(error_response, status=status.HTTP_401_UNAUTHORIZED)

    # 403 permission denied responses
    if isinstance(exc, drf_exceptions.PermissionDenied):
        error_response = {
            "message": "You do not have permission to perform this action."
        }
        return Response(error_response, status=status.HTTP_403_FORBIDDEN)

    # 405 bad request response
    if isinstance(exc, drf_exceptions.MethodNotAllowed):
        method = exc.args[0] if exc.args else ""
        error_response = {"message": f"Method {method} not allowed."}
        return Response(error_response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # if none of the above cases checked true, call the default drf exception handler
    response = exception_handler(exc, context)
    return response
