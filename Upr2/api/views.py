from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.backend_user import create_user


class UserRegisterView(APIView):

    def post(self, request):
        msg = create_user(request)
        return Response(data=msg, status=status.HTTP_200_OK)