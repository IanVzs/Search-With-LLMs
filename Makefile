run:
	@if [ ! -d "venv" ]; then \
		@$(MAKE) -f Makefile usevenv; \
	else \
		echo "use venv"; \
	fi
	venv/bin/python main.py

usevenv:
	@if [ ! -d "venv" ]; then \
		python3 -m venv venv; \
		echo "venv created"; \
	else \
		echo "venv already exists"; \
	fi
	venv/bin/python -m pip install -r requirements.txt

build:
	cd web && npm install && npm run build
