from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import LoginSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(
        name="post",
        decorator=swagger_auto_schema(
            operation_description="Registration",
            operation_summary="The route is registration user",
            tags=["Auth"],
        ),
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Token.objects.create(user=user)
            return Response(
                {
                    "message": "User registered successfully!",
                    "token": Token.objects.get(user=user).key,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_description="Login",
        operation_summary="The route is login user",
        tags=["Auth"],
    ),
)
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_description="Logout",
        operation_summary="The route is logout user",
        tags=["Auth"],
    ),
)
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "Successfully logged out."}, status=204)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
