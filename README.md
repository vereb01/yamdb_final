![vereb01/yamdb_final](https://github.com/vereb01/yamdb_final-1/actions/workflows/yamdb_workflow.yml/badge.svg)

Проект доступен по адресу http://158.160.44.240/api/v1/

yamdb_final (API YaMDb)
API интернет-сервиса YaMDB для хранения рецензий на произведения
Описание проекта API YaMDB:
Проект YaMDb собирает рецензии пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка» и другие, также произведениям могут быть присвоены жанры. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Зарегистрированные пользователи могут оставить к произведениям текстовые отзывы и поставить произведению оценку в диапазоне от одного до десяти, из пользовательских оценок формируется рейтинг произведения. На одно произведение пользователь может оставить только один отзыв. Также пользователи могут комментировать отзывы о произведениях. Предусмотрен функционал для модерирования отзывов и комментариев к отзывам. Анонимные пользователи могут просматривать описания произведений, читать отзывы и комментарии.


Стек: Python 3.7, Django, DRF, Simple-JWT, PostgreSQL, Docker, nginx, gunicorn, GitHub Actions (CI/CD).

### Шаблон наполнения env-файла:
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres 
    DB_HOST=db
    DB_PORT=5432 

### Развертывание проекта:

Клонируем репозиторий к себе на ПК:

```bash
  git clone https://github.com/vereb01/yamdb_final.git
```

Переходим в дерикторию с проектом:

```bash
  cd yamdb_final
  cd api_yamdb
```

Устанавливаем Виртуальное окружение:

```bash
  python -m venv venv
```

Активируем виртуальное окружение:

```bash
  source venv/Scripts/activate
```

Устанавливаем зависимости:

```bash
  pip install -r requirements.txt
```

Переходим в папку с файлом docker-compose.yaml:

```bash
  cd infra
```

Поднимаем контейнеры:

```bash
  docker-compose up -d --build
```

Выполняем миграции:

```bash
  docker-compose exec web python manage.py makemigrations reviews

  docker-compose exec web python manage.py migrate
```

Создаем суперпользователя:

```bash
  docker-compose exec web python manage.py createsuperuser
```

Србираем статику:

```bash
  docker-compose exec web python manage.py collectstatic --no-input
```
Cоздать резервную копию БД командой:

```bash
docker-compose exec web python manage.py loaddata fixtures.json
```


