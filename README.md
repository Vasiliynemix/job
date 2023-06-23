alembic init migrations

from myapp import mymodel

alembic revision --autogenerate -m 'comment'

alembic upgrade head
