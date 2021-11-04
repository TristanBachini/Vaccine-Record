//configuring mysql
sudo mysql_secure_installation
sudo mysql
CREATE USER 'db_username'@'localhost' IDENTIFIED BY 'password';

//IF password policy requirements not met
SHOW VARIABLES LIKE 'validate_password%';
SET GLOBAL validate_password.length = 5;
SET GLOBAL validate_password.number_count = 0;
SET GLOBAL validate_password.policy=LOW;

CREATE USER 'db_username'@'localhost' IDENTIFIED BY 'password';

//creating the database
CREATE DATABASE db_name;
GRANT ALL PRIVILEGES ON * . * TO 'db_username'@'localhost';
FLUSH PRIVILEGES;
\q

//Database environments
DATABASE_ENGINE=django.db.backends.mysql
DATABASE_VACCINE=db_name
DATABASE_PASSWORD=password
DATABASE_USER=db_username

//if "Table 'vax_record.auth_user' doesn't exist"
python manage.py migrate auth
python manage.py makemigrations
python manage.py migrate

//creating a superuser
python manage.py createsuperuser

//To activate virtual env
pipenv shell

//Installed packages
pip install -r requirements.txt 

//incase the above code did not work:
pip install xhtml2pdf
sudo apt-get install libmysqlclient-dev
sudo -H pip3 install mysqlclient
pip install django_filter
pip install Django==3.2.8
pip install django-crispy-forms

//To run
python manage.py runserver
//login using created superuser

//go to patient>create patient
//will be greeted with this error: django.contrib.auth.models.Group.DoesNotExist: Group matching query does not exist.
//to fix
//go to http://127.0.0.1:8000/admin/
//create group named 'patient'

//to collect static everytime may changes sa static files
//python manage.py collectstatic