install_deps:
	@poetry install --remove-untracked

generate_test_graphql_schema:
	@./manage.py graphql_schema --schema server.gql.schema --out tests/schema.graphql

lint:
	@./scripts/lint.sh

test:
	@pytest

make_messages:
	@./manage.py makemessages --ignore=.venv/* -l en --no-location

compile_messages:
	@./manage.py compilemessages

pre_commit:
	@pre-commit

install_pre_commit:
	@pre-commit install && pre-commit install --hook-type commit-msg

update_pre_commit:
	@pre-commit autoupdate
