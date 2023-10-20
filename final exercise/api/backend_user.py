
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth import login, authenticate
from knox.models import AuthToken
from .serializers import UserSerializerSearchByUsername
from .backend_utils import findUser


def create_user(request) -> dict:
    """
    User creation method
    gets username, email, password, password_check checks if the info is valid, and if everything is ok, creates user
    then return info
    """

    # data request
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_check = request.data.get('password_check')
    
    # validate email uniqness
    if User.objects.filter(email=email).exists():
        return {'This email is already in use!'}
    # validate username uniqueness
    if User.objects.filter(username=username).exists():
        return {'Error': 'the username is already in use!'}
    # validate email len
    if len(str(email))==0:
        return {'Error': 'Email was not provided!'}
    # validate username len
    if len(username) <= 2:
        return {'Error', f'the username: {username} is too short'}
    # validate password
    if len(password) < 8:
        return {'Error': 'the password is too short!'}
    if password != password_check:
        return {'Error': 'the passwords do not match!'}
    
    # convert the pass to hash
    hashed_password = make_password(password)

    # create user
    user = User(
        username=username,
        email=email,
        password=hashed_password,
        is_active=True
    )
    user.save()
    info = f'Account with username: {username} was created!'
    
    return info


def get_user(request):
    """Get user's username"""
    username = request.data.get('username')

    try:
        user = User.objects.get(username=username)
        serialized = UserSerializerSearchByUsername(user)
    except User.DoesNotExist:
        return {'Error': 'The user does not exist!'}

    return serialized


def login_user(request) -> dict:
    """Login method"""
    username = request.data.get('username')
    password = request.data.get('password')
    ERROR = {'Error': 'Invalid credintials!'}

    try:
        user_obj = User.objects.get(username=username)
    except User.DoesNotExist:
        return ERROR

    if not user_obj.is_active:
        return {'Error': 'You must activate your email first and then login'}
    flag = authenticate(request, username=username, password=password)
    if flag:
        logged_devices = AuthToken.objects.filter(user=user_obj).count()
        if logged_devices >= 4:
            return {'Error': 'Maximum limit of logged devices is reached!'}
        token = AuthToken.objects.create(user_obj)
        print(token)
        login(request, flag)
        serialized = UserSerializerSearchByUsername(user_obj)
        return serialized
    else:
        return ERROR
    

def edit_profile(request) -> dict:
    """Edit profile method"""
    token = request.META.get('HTTP_AUTHORIZATION')
    user = findUser(token)
    method = request.data.get('method')
    #TODO: add request method func
    if user is None:
        return {'Error': 'User not found!'}
    else:
        if method == 'password':
            password = request.data.get('password')
            password_check = request.data.get('password_check')
            # validate password
            if len(password) < 8:
                return {'Error': 'the password is too short!'}
            if password != password_check:
                return {'Error': 'the passwords do not match!'}
            user.set_password(password)
            user.save()
            return {'Successs': 'Password changed successfully!'}
        else:
            return {'Error': 'Please select what you want to edit!'}


def delete_profile(request) -> dict:
    """Delete profile method"""
    token = request.META.get('HTTP_AUTHORIZATION')
    user = findUser(token)
    
    if user is None:
        return {'Error': 'User not found!'}
    else:
        username = user.username
        User.objects.filter(username=username).delete()
        return {'Success': 'You have successfully deleted your account!'}
    