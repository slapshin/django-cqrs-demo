#!/usr/bin/env sh

set -o errexit
set -o nounset

run_checkers() {
  black --check .

  mypy .

  flake8 .

  # Run checks to be sure settings are correct (production flag is required):
#  DJANGO_ENV=production python manage.py check --deploy --fail-level WARNING

  # Running code-quality check:
  xenon --max-absolute A \
        --max-modules A \
        --max-average A \
        --exclude server/apps/core/graphql/fields/query_connection.py \
        server

  # Check that all migrations worked fine:
  DJANGO_ENV=build python manage.py makemigrations --dry-run --check

  # Checking `pyproject.toml` file contents:
  poetry check

  # Checking dependencies status:
  pip check

  # Checking if all the dependencies are secure and do not have any
  # known vulnerabilities:
#  safety check --bare --full-report -i 39462

  # po files
  polint -i location,unsorted locale

  if find locale -name '*.po' -print0 | grep -q "."; then
    # Only executes when there is at least one `.po` file:
    dennis-cmd lint --errorsonly locale
  fi
}

run_checkers
