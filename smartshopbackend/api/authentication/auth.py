from functools import wraps
from rest_framework.response import Response
from api.models import AuthToken, User


def auth_wrapper(func):
    def inner(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
             return Response({"error": "Token missing in the header"}, status=400)
        token = AuthToken.objects(token=token).first()
        if not token or not token.is_valid():
            return Response({"error": "Auth failure"}, status=400)
        request.user = User.objects(id=token.user)
        result = func(request, *args, **kwargs)
        return result
    return inner
