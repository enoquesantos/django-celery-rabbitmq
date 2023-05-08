# django-celery-rabbitmq
A pure simple Django + Celery + RabbitMQ project

## start and run with docker
```
cd docker
docker-compose up
```

## open django in browser
```
http://localhost:8000
```

## start and run manually
### Create the .env
1. Create a copy of application.env.example in application folder
2. Add the .env parameters

### Create the virtual environment
```
python3 -m venv .venv
```

### Start the virtual environment
```
source .venv/bin/activate
```

### Install dependencies
```
pip3 install --no-cache-dir -r requirements.txt
```

### Create the dependencies file for production with all lib version
```
pip3 freeze > requirements-production.txt
```

### Create the migrations
```
python3 manage.py makemigrations auth django_celery_results post_office abstract post
```

### Apply the migrations to database
```
python3 manage.py migrate
```

### Create the Django superuser
```
python3 manage.py createsuperuser
```

### Start the celery
```
** run this command in separate terminal tab/window into projetct virtualenv **
celery --app application worker -l INFO
```

### Start the celery beat for schedule tasks
```
** run this command in separate terminal tab/window into projetct virtualenv **
celery --app application beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### Start the Django
```
python3 manage.py runserver 0.0.0.0:8000
```
