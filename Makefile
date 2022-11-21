# -- poetry --

poetry-install:
	@poetry install --remove-untracked

# -- code --

lint:
	black --check .
	mypy .
	flake8 .
	DJANGO_ENV=build python manage.py makemigrations --dry-run --check
	xenon --max-absolute A \
        --max-modules A \
        --max-average A \
        --exclude server/apps/core/graphql/fields/query_connection.py \
        server
	poetry check
	pip check
	#  safety check --bare --full-report -i 39462
	polint -i location,unsorted locale
	dennis-cmd lint --errorsonly locale

test:
	@pytest

# -- django --

make-messages:
	@python manage.py makemessages --ignore=.venv/* -l en --no-location

compile-messages:
	@python manage.py compilemessages

# -- pre-commit --

pre-commit:
	@pre-commit

pre-commit-install:
	@pre-commit install
	@pre-commit install --hook-type commit-msg

pre-commit-update:
	@pre-commit autoupdate
