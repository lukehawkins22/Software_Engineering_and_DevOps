# Software_Engineering_and_DevOps
This ReadMe document can be used to learn about the Help Desk application.

This application is running and accessible here:

Eng Environment: https://it-help-desk-eng.onrender.com/
Prod Environment: https://it-help-desk.onrender.com/

Admin page is accessible via the link at the bottom of the homepage, or directly here:
https://it-help-desk.onrender.com/admin/login/?next=/admin/ or
https://it-help-desk-eng.onrender.com/admin/login/?next=/admin/

Please conduct all admin actions via the admin interface. 
Admin Account Username: qaadmin
Admin Account Password: QAtutor123

Feel free to create new users and tickets to test functionality

Dependencies:
1. Python (Latest Version Preferable)
2. Django Web Framework (Latest Version Preferable)
3. This GitHub Repository
4. Web browser of your choice

See requirements.txt for a list of all required python packages.

Installation:
To install and setup this application, follow the below steps.
1. Install Python. This must be installed on the machine running the app and it must be accessible from the application directory. An example Ubuntu command to install Python can be seen below:
```bash
sudo apt-get update
```
```bash
sudo apt install python3-pip -y
```
2. Install dependencies framework. This can be done by following steps listed here https://docs.djangoproject.com/en/4.1/intro/install/. An example Ubuntu command to install Django and other dependencies can be seen below:
```bash
pip install -r requirements.txt
```
3. Clone this code repository to the server which you want to run the application on. It needs to run in the location where Django and Python have access to. 
```bash
git clone https://github.com/lukehawkins22/Software_Engineering_and_DevOps.git
```
4. When ready to launch, start the application by running this command in the top level git repo folder. 
For running on server:
```bash
python startup.py
```
For running on LocalHost:
```bash
python manage.py collectstatic
python manage.py runserver 
```

Unit tests can be found here: ITHelpDesk/tests. There are 2 test files, test_forms.py and test_views.py. Commands to run these can be found as a comment at the top of each file.

Application Files:
1. admin.py: Used to handle the configuration of the Django Admin Interface. Different object views and setups are configured within these files.
2. apps.py: Used to handle high level application configuration. Little detail within this file.
3. forms.py: Used to define and generate all forms which are used throughout the app. Forms are used to present and collect data from the user which is then used throughout the application. There are multiple types of form which are used within this app.
4. models.py: Used to define all data models which are used to store data for the application to be functional. This includes the 'ticket' and 'comment' model which are used consistently throughout the application
5. tests.py: Not used as using Pytest. To execute tests, see test folder. At the top of each test file is a command which should be run in terminal within this repo folder. This will execute the tests and display results. 
6. urls.py: Used to define URL routings, and which views should be served when a certain URL is requested. There are 2 urls.py files. One at a project level, and one at an application level. The majority of the config is complete within the application level file. The project level file inherits from the application level to handle requests.
7. views.py: Used to handle the rendering of views, as well as functions and methods which should be executed should a view be called or rendered based on a URL request. This is the file which is responsible for defining what should be rendered when a page is visited. 

The below files are at a project level;
1. settings.py: Used to define project level config settings. This included things such as links to the application level files, as well as numerous Django configuration properties. 
2. urls.py: As discussed above, this handles inherits details from the application level file and handled requests appropriately. 
3. manage.py: Defines Djangos cmd functions for admin related tasks.

The asgi.py, wsgi.py and __init__.py files are used for Django config only. No changes have been made to these files. 

Database: The db.sqlite3 file is the database which is used within the application. these relate to the models.py file, and this acts as an ORM solution to perform CRUD operations on the SQLiteDB. 

Throughout this application, there are a number of different classes, methods and functions used. The purpose behind each of these can be located within the code comments in the individual .py files. These provide a comprehensive overview of the purpose of each section of code. 

