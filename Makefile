install:
	poetry install

gd:
	poetry run gendiff 

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 gendiff
	poetry run mypy gendiff

pytest:
	poetry run pytest -vv

cover:
	poetry run pytest --cov=gendiff tests/ --cov-report xml
