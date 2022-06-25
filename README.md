University Schedule Backend
======================================

```
docker-compose build
docker-compose up
```

 - ```http://127.0.0.1:8000/docs``` - дока
 - ```/templates``` - шаблоны
 - ```/static``` - css, js


# .env example
```
APP_ENV="dev"
```

# .env.dev example
```
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
SECRET_KEY = "123"
```
