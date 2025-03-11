main:
	. .env/bin/activate && python -O main.py
debug:
	. .env/bin/activate && python main.py
test:
. .env/bin/activate && python test.py

