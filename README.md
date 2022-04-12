# PostBeyond test api

## Using with docker container (preferably)
1. Run `docker-compose up -d`
2. Open `http://localhost/v0_1/docs`


## Using in local development mode
### Setup Python Virtual Environment for local development
1. Install virtualenv: `pip install virtualenv`
2. Create new virtual environment.
    * Unix-based: `virtualenv -p python3 venv`
3. Activate created virtualenv.
    * Unix-based: `. venv/bin/activate`
4. Under project root directory write the next command `pip install -r requirements.txt`
### Setup ENV variables
1. DATABASE_URL: `export DATABASE_URL=<database_url>`
 (For example "postgresql+psycopg2://postgres:test@api_db:5432/api_db") if we run db from "api_db" container).
2. PYTHONPATH: `export PYTHONPATH=<absolute path to directory>`
### Run alembic
1. Run `alembic upgrade head`
### Start app
1. Run `python app/main.py` *to run app you need to set up Postgres.app to your machine
2. Open `http://127.0.0.1:8080/v0_1/docs`

## Alembic
1. After having any changes in schema run `alembic revision --autogenerate -m "<commit message>"`
2. To upgrade db run `alembic upgrade head`

## Psycopg2
For example for Macs you need to `Postgres.app` to be installed
1. In terminal type `export PATH=/Applications/Postgres.app/Contents/Versions/13/bin/:$PATH`
2. Run `pip install psycopg2`


#TODO
1. Create an extended version of logger (instead of prints)
2. Add new field to Group instance (description, some characteristics, etc.)
3. Extend User entity (age, profession, address, phone, etc.)
4. Implement authorization to restrict role and status changing by administrators only
5. Implement possibility to change User's data. Allow access only for themselves or administrators
6. Implement filtration and pagination for users and groups
7. Extend email verification, checking whether email exists in real world or not
8. Add endpoints for getting exact Group or User info
9. Extend deleting mechanism
10. Create scalable mechanism to add initial data to db
11. Add new API versions
12. Add tests





  