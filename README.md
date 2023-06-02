![vereb01/yamdb_final](https://github.com/vereb01/yamdb_final-1/actions/workflows/yamdb_workflow.yml/badge.svg)

Проект доступен по адресу http://158.160.44.240/api/v1/
b yt 

yamdb_final (API YaMDb)
API интернет-сервиса YaMDB для хранения рецензий на произведения
Описание проекта API YaMDB:
Проект YaMDb собирает рецензии пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка» и другие, также произведениям могут быть присвоены жанры. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Зарегистрированные пользователи могут оставить к произведениям текстовые отзывы и поставить произведению оценку в диапазоне от одного до десяти, из пользовательских оценок формируется рейтинг произведения. На одно произведение пользователь может оставить только один отзыв. Также пользователи могут комментировать отзывы о произведениях. Предусмотрен функционал для модерирования отзывов и комментариев к отзывам. Анонимные пользователи могут просматривать описания произведений, читать отзывы и комментарии.

Стек: Python 3.7, Django, DRF, Simple-JWT, PostgreSQL, Docker, nginx, gunicorn, GitHub Actions (CI/CD).

