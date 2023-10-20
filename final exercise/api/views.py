from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .backend_user import create_user, get_user, login_user, edit_profile, delete_profile
from django.http import JsonResponse
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication


class UserRegisterView(APIView):
    """User register"""
    permission_classes = (AllowAny,)

    def post(self, request):
        return handle_response(create_user(request))
    

class UserLogin(KnoxLoginView):
    """User login"""
    permission_classes = (AllowAny,)
    
    def post(self, request):
        return handle_response_data(login_user(request))
    

class UserProfile(APIView):
    """User S.E.D(search, edit, delete)"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request):
        return handle_response(edit_profile(request))
        
    def delete(self, request):
        return handle_response(delete_profile(request))
        
    def get(self, request):
        return handle_response_data(get_user(request))
    
#Supp funcs

def handle_response(msg):
    if isinstance(msg, dict) and 'Error' in msg.keys():
        return JsonResponse(data=msg, status=status.HTTP_400_BAD_REQUEST)
    else:
        # If the obj is type set return list(obj)
        if isinstance(msg, set):
            return JsonResponse(data=list(msg), status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse(data=msg, status=status.HTTP_200_OK, safe=False)


def handle_response_data(msg):
    if isinstance(msg, dict) and 'Error' in msg.keys():
        return JsonResponse(data=msg, status=status.HTTP_200_OK, safe=False)
    else:
        return JsonResponse(data=msg.data, status=status.HTTP_200_OK)