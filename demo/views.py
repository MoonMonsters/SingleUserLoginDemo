
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework import status

from demo.utils.cache import cache_set_user_token
from demo.utils.authentications import UserTokenAuthentication

# 将用户数据添加进载荷
# /rest_framework_jwt/utils.py jwt_payload_handler函数
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# 加密
# /rest_framework_jwt/utils.py jwt_encode_handler函数
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class LoginView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 用户对象
            user = serializer.object.get('user') or request.user
            # token
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            cache_set_user_token(user, token, api_settings.JWT_EXPIRATION_DELTA)
            return Response(response_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookView(generics.GenericAPIView):
    authentication_classes = [UserTokenAuthentication, ]

    def get(self, request, *args, **kwargs):

        return Response({'user': request.user.id}, status=status.HTTP_200_OK)
