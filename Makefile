install:
	poetry init
	cat requirements.txt | xargs poetry add
	poetry install --no-root
	poetry add pre-commit
	pre-commit install
pre-commit:
	pre-commit run --all-files
run:
	poetry run python main.py
clean:
	rm -r -f cache
	rm -r -f profiles
	rm -r -f tasks
	rm -f local_storage.json
	rm -f profiles.json
clean_all:
	make clean
	rm -r -f output
