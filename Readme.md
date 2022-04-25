# Description


# Start

### depends
python3.9.10
virtualenv

django
djangorestframework
djangorestframework-simplejwt
psycopg2
django-cors-headers

`$ pip install django djangorestframework djangorestframework-simplejwt psycopg2 django-cors-headers django-environ`


`settings/settings.py`

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'auth
]

MIDDLEWARE = [
    ...,
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...,
]
```

### postgresql

#### 2.1- Install postgres and create database

##### 1**.- Install PostgresSQl**

```
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
$ sudo apt-get update
$ sudo apt-get -y install postgresql postgresql-contrib
$ sudo apt-get install libpq-dev
```

##### **2.- execute postgresql**

```
$ sudo service postgresql status
$ sudo service postgresql start
```

##### **3.- Create database and password**

```
sudo -u postgres psql => start console
```
```
postgres=# alter user Postgres with password 'newPasword';
postgres=# CREATE DATABASE name;
```

- set this dates in your .env

```
POSTGRES_NAME=name
POSTGRES_PASSWORD=newPasword
```


```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("POSTGRES_NAME"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": "5432",
    }
}
```

### .env vars


Configure env
`settings/settings.py`

```py 
import environ                     
import os
env = environ.Env(                
    # set casting, default value
    DEBUG=(bool, False)         
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))  
```

# Base de datos

# algoritmo de repeticion espaciada


1. Calidad: La calidad de recordar la respuesta de una escala de 0 a 5.
    5. : respuesta perfecta.
    4. : respuesta correcta después de una vacilación.
    3. : respuesta correcta recordada con seria dificultad.
    2. : respuesta incorrecta; donde el correcto parecía fácil de recordar.
    1. : respuesta incorrecta; el correcto recordado.
    0. : apagón completo.
2. Facilidad: El factor de facilidad, un multiplicador que afecta el tamaño del intervalo, determinado por la calidad del recuerdo.
3. Intervalo: La brecha/espacio entre su próxima revisión.
4. Repeticiones: el recuento de respuestas correctas (calidad >= 3) que tiene seguidas.