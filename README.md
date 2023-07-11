**Instalar dependencias**

`pip install -r requirements.txt`


**Migraciones:**

Para crear las migraciones:

`alembic revision --autogenerate -m "Added account table"
`

Para aplicar las migraciones:

`alembic upgrade head
`

**Levantar APP**

`sh startapp.sh`

**Flake8 + Test + Coverage**

`sh run_tests.sh`