# -- poetry --

poetry-install:
	poetry install --remove-untracked

# -- code --

lint:
	black --check .
	mypy .
	flake8 .
	DJANGO_ENV=build python src/manage.py makemigrations --dry-run --check
	xenon --max-absolute A \
        --max-modules A \
        --max-average A \
        --exclude src/apps/core/graphql/fields/query_connection.py \
        src
	poetry check
	pip check
	#  safety check --bare --full-report -i 39462
	polint -i location,unsorted src/locale
	dennis-cmd lint --errorsonly src/locale

test:
	pytest

# -- django --

make-messages:
	python src/manage.py makemessages -l en --no-location

compile-messages:
	python src/manage.py compilemessages

# -- pre-commit --

pre-commit:
	pre-commit

pre-commit-install:
	pre-commit install
	pre-commit install --hook-type commit-msg

pre-commit-update:
	pre-commit autoupdate
