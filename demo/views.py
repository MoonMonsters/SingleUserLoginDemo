from rest_framework import generics
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework import status

from demo.utils.cache import cache_set_user_token
from demo.utils.authentications import UserTokenAuthentication
from demo.utils.serializers import UserSerializer


# jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
# 将用户数据添加进载荷
# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# 加密
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 用户对象
            user = serializer.object.get('user') or request.user
            # token
            # 此处用了框架自带的函数，token中只保存了user的某些数据
            # 也可以按照jwt_payload_handler, jwt_encode_handler两个函数(路径: /rest_framework_jwt/utils.py)任意添加
            token = serializer.object.get('token')
            # 框架实现的函数中，只加入了token值，可以自己按需求返回数据，不一定使用此函数
            # response_data = jwt_response_payload_handler(token, user, request)
            response_data = self._jwt_response_payload_handler(token, user, request)

            # 将token值加入redis缓存中，以此来实现单用户登录
            cache_set_user_token(user, token, api_settings.JWT_EXPIRATION_DELTA)
            return Response(response_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _jwt_response_payload_handler(token, user, request):
        return {
            'token': token,
            'user': UserSerializer(user).data,
            # 'request': request
        }


class BookView(generics.GenericAPIView):
    authentication_classes = [UserTokenAuthentication, ]

    def get(self, request, *args, **kwargs):
        """
        模拟数据
        """
        user_data = UserSerializer(self.request.user).data
        return Response(user_data, status=status.HTTP_200_OK)
