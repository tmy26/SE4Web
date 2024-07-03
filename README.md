# First steps in Django
### This project was created for educational purposes while I was teaching at Plovdiv University, its main goal is to introduce students to Python and Django.



### How to create new project
1. Create new folder
2. Check if python is installed
    ```
    python --version
    ```
3. Create virtual environment
    ```
    python -m venv venv
    ```
4. Launch the virtual environment(venv)
    ```
    For windows:
    	.\venv\Scripts\activate
    For MacOs:
    	source venv/bin/activate
    ```
5. Install the needed libraries
    ```
    pip install django djangorestframework
    ```
6. Create project
    ```
    django-admin startproject webapp .
    ```
7. Create app
    ```
    django-admin startapp api
    ```
8. Open your VSCode and navigate to webapp_settings.py and in INSTALLED_APPS add the following:
    ```
    'rest_framework',
    'rest_framework.authtoken'
    'api', 
    ```
9. Navigate to webapp_urls.py and add the following
    ```
    #path('', include('api.urls')),
    ```
10. Create urls.py in api folder

### If you managed to follow all the steps, now you just have to 'makemigrations' and 'migrate'
	python manage.py makemigrations
	python manage.py migrate
*Use 'python manage.py makemigrations' when u have added a library or created/made changes to a model in the db! Then use python manage.py migrate to apply the changes!*

11. Create super user with the following command
    ```
    python manage.py createsuperuser
    ```
12. Start the server
    ```
    python manage.py runserver
    ```
### Finally login in to the admin panel - http://127.0.0.1:8000/admin/
