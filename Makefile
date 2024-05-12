install:
	poetry install --no-root
run:
	poetry run python main.py
clean:
	rm -r -f cache
	rm -r -f profiles
	rm -r -f tasks
	rm -r -f error_logs
	rm -f local_storage.json
	rm -f profiles.json
clean_all:
	make clean
	rm -r -f output
