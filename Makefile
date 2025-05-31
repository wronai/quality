.PHONY: setup dev test quality clean

setup:
	pip install -r requirements.txt
	python setup_quality_guard.py --local

dev:
	python main.py

test:
	python -m pytest tests/ -v

quality:
	python setup_quality_guard.py --check-project

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -f quality-violations.log
	rm -f quality-report-*.html

help:
	@echo "Dostępne komendy:"
	@echo "  setup   - Instalacja zależności i Quality Guard"
	@echo "  dev     - Uruchomienie w trybie deweloperskim"
	@echo "  test    - Uruchomienie testów"
	@echo "  quality - Sprawdzenie jakości kodu"
	@echo "  clean   - Czyszczenie plików tymczasowych"