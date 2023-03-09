## 🗒 Notes system

This is a simple Django web application that allows users to create, view,
update and delete notes via a REST API. Users can register,
log in and log out to access their own notes.
Each note has a title, description and creation date.

### Requirements

- 🔐 Users must be able to register, log in and log out.
- ✍️ Users should be able to create, view, update and delete notes via REST api.
- 📅 Each note must have a title, description and creation date.
- 🔖 Users should only be able to view, update and delete their own notes.
- 🧪 Api endpoints should be covered by tests.
- 🛡️ Protection against common web application attacks.

### Local deployment

```bash
python3 -m venv env
source env/bin/activate
pip install poetry
poetry install
```

Create .env file, extract the virtual environment variables into the .env file (you can find an example in env.example)

```bash
./manage.py migrate
./manage.py runserver
```

Run tests

```bash
./manage.py test
```

Run linting and formatting

```bash
flake8 . --count --statistics --show-source &&
black . && 
isort --check . && 
bandit -r .
```

### Docker deployment

* Watch commands in the Makefile

```bash
make help
```

* Build docker image

```bash
make build
```

* Run docker container

```bash
make up
```

* Run tests

```bash
make test
```

* Stop docker container

```bash
make down
```

* Clean all docker containers

```bash
make prune
```

### Technologies

- Python 3.11
- Django 4.1.7
- Django REST Framework 3.14.0
- Docker 20.10.17
- Poetry 1.1.11
- Nginx 1.21.3
