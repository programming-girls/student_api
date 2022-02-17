# Eshirali School API

Eshirali School is an online platform where students and parents can sign up to get access to exam and marking scheme material from different schools and the official KNEC KCPE and KCSE exams.

Exams can either be done on the platform and marked by the system, or can be downloaded to be done physically. 

# Installation

using github:

clone the repo to server/localhost

```git clone https://github.com/programming-girls/student_api.git```

install virtualenv

```virtualenv venv```

activate venv

``` source venv/bin/activate ```

install requirements

```pip install -r requirements.txt ```

install .env

``` source .env```

Perform migrations

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 data/loaddata.py -f data/user_data.json
```


Testing

```python manage.py test```

# Running the app

```export FLASK_APP=app.py```

Start the server

```flask run```

# Endpoints

AUTH

| HTTP REQUEST | URL                     | PARAMS                                               |
|--------------|-------------------------|------------------------------------------------------|
| [GET, POST]  | /register/              | {'email':'email@email.com', 'password':'email@1234'} |
| [GET, POST]  | /login                  | {'email':'email@email.com', 'password':'email@1234'} |
| [GET, POST]  | /forgot_password        | {'email':'email@email.com'}                          |
| [GET, POST]  | /change_password        | {'password:'lol112', 'new_password':'lol112'}        |
| [GET, POST]  | /reset_password/<token> | {'password':'email@12345'}                           |
| [POST]       | /logout                 | N/A                                                  |
| [GET, POST]  | /google_login           | N/A                                                  |
| [GET, POST]  | /facebook_login         | N/A                                                  |


CHILD

| HTTP REQUEST                             | URL                         | PARAMS |
|------------------------------------------|-----------------------------|--------|
| ['GET' ,  'POST' ,  'PUT' ,  ' DELETE '] | /child                      |        |
| ['GET' ,  'POST' ,  'PUT' ,  ' DELETE '] | /child/<int:child_id>/exams |        |


PARENT

| HTTP REQUEST                             | URL                                           | PARAMS |
|------------------------------------------|-----------------------------------------------|--------|
| ['GET' ,  'POST' ,  'PUT' ,  ' DELETE '] | /parent                                       |        |
| ['GET' ,  'POST' ,  'PUT' ,  ' DELETE '] | /parents_child/<int:parent_id>/<int:child_id> |        |
