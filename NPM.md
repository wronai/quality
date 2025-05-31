
# 🛡️ Interpreter-Level Code Quality Control

## 🎯 Kompletny Przewodnik Implementacji

### Jak to działa:
Zamiast zwykłego uruchomienia:
```bash
python main.py
npm start
node server.js
```

Otrzymujesz:
```bash
🔍 Sprawdzanie jakości kodu: main.py
==================================================
❌ BŁĘDY KRYTYCZNE (kod nie może być uruchomiony):
  ❌ main.py:45
     Funkcja 'process_data' ma 75 linii (maksimum: 50)
     💡 Podziel funkcję na mniejsze, bardziej specjalizowane funkcje

  ❌ main.py:120
     Plik ma 300 linii (maksimum: 200)
     💡 Podziel plik na mniejsze moduły

🚫 Wykonanie przerwane z powodu problemów z jakością kodu
   Napraw powyższe problemy i spróbuj ponownie
```

## 📦 Instalacja (3 minuty)

### Krok 1: Pobierz Quality Guard
```bash
# Utwórz katalog dla Quality Guard
mkdir quality-guard && cd quality-guard

# Pobierz pliki (lub skopiuj z artifacts)
curl -O https://raw.githubusercontent.com/your-repo/interpreter_quality_guard.py
curl -O https://raw.githubusercontent.com/your-repo/npm-quality-wrapper.sh

# Lub skopiuj z artifacts powyżej
```

### Krok 2: Inicjalizacja
```bash
# Zainicjalizuj w swoim projekcie
python interpreter_quality_guard.py --init

# To utworzy:
# ✅ quality-config.json (konfiguracja)
# ✅ python-quality-wrapper.py (wrapper dla Python)
# ✅ nodejs-quality-wrapper.js (wrapper dla Node.js)
# ✅ npm-quality-wrapper.sh (wrapper dla NPM)
# ✅ setup-quality-aliases.sh (skrypt aliasów)
```

### Krok 3: Aktywacja Aliasów
```bash
# Ustaw aliasy (automatyczne)
./setup-quality-aliases.sh

# Przeładuj shell
source ~/.bashrc  # lub ~/.zshrc

# Gotowe! Teraz każde uruchomienie będzie sprawdzane
```

## ⚙️ Konfiguracja

### quality-config.json
```json
{
  "max_file_lines": 200,
  "max_function_lines": 50,
  "max_function_params": 4,
  "max_nesting_depth": 4,
  "max_complexity": 10,
  "max_class_methods": 15,
  "required_docstrings": true,
  "strict_mode": true,
  "forbidden_patterns": [
    "eval(",
    "exec(",
    "globals()",
    "__import__",
    "console.log"
  ]
}
```

### Tryby działania:
```json
{
  "strict_mode": true,    // Blokuje przy ostrzeżeniach
  "strict_mode": false    // Blokuje tylko przy błędach
}
```

## 🎯 Przykłady Użycia

### Python
```bash
# Przed (normalne uruchomienie):
python main.py

# Po (z kontrolą jakości):
python main.py
🔍 Sprawdzanie jakości kodu: main.py
==================================================
✅ Kod spełnia wszystkie standardy jakości!
🚀 Uruchamianie kodu...
# Tutaj normalny output programu
```

### Node.js/NPM
```bash
# Przed:
npm start
node server.js

# Po:
npm start
🛡️ NPM Quality Guard aktywny...
🔍 Sprawdzanie jakości kodu...
📁 Sprawdzanie 15 plików...
  ✅ src/server.js - OK
  ✅ src/routes/api.js - OK
  ❌ src/utils/helpers.js:45 - Funkcja ma 65 linii (maksimum: 50)
📦 Sprawdzanie package.json...
  ✅ Wszystkie wymagane skrypty obecne
🔒 Sprawdzanie bezpieczeństwa zależności...
  ✅ Brak podatności w zależnościach
🚫 Wykonanie NPM przerwane z powodu problemów z jakością kodu
```

## 🔧 Zaawansowane Opcje

### Wrapper bez Aliasów
```bash
# Bezpośrednie użycie wrapper'ów
./python-quality-wrapper.py main.py
./nodejs-quality-wrapper.js server.js
./npm-quality-wrapper.sh start
```

### Pomijanie Kontroli (Emergency)
```bash
# Użyj pełnej ścieżki do oryginalnego interpretera
/usr/bin/python main.py        # Pomija kontrolę
/usr/bin/node server.js        # Pomija kontrolę
$(which npm) start             # Pomija kontrolę
```

### Kontrola Selektywna
```bash
# Sprawdź tylko konkretny plik
python interpreter_quality_guard.py main.py

# Wynik:
# ✅ Kod może być uruchomiony
# LUB
# 🚫 Kod nie może być uruchomiony
```

## 📊 Monitorowanie i Logi

### Logi Jakości
```bash
# Automatyczne logi w:
quality-violations.log

# Format JSON:
{
  "timestamp": "2024-01-15T10:30:00Z",
  "file": "main.py",
  "violations": [
    {
      "type": "FUNCTION_TOO_LONG",
      "line": 45,
      "message": "Funkcja 'process_data' ma 75 linii",
      "severity": "error"
    }
  ]
}
```

### Dashboard (Opcjonalny)
```bash
# Generuj raport HTML
python interpreter_quality_guard.py --report

# Tworzy: quality-report.html
```

## 🚀 Integracja z Zespołem

### Git Hooks + Interpreter Control
```bash
# .husky/pre-commit
#!/bin/sh
# Sprawdź wszystkie pliki przed commitem
find src -name "*.py" -exec python interpreter_quality_guard.py {} \;
find src -name "*.js" -exec node nodejs-quality-wrapper.js {} \;
```

### CI/CD Integration
```yaml
# .github/workflows/quality.yml
name: Quality Control
on: [push, pull_request]
jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Quality Guard
      run: |
        python interpreter_quality_guard.py --init
    - name: Check Python Files
      run: |
        find . -name "*.py" -exec python interpreter_quality_guard.py {} \;
    - name: Check JS Files  
      run: |
        find . -name "*.js" -exec node nodejs-quality-wrapper.js {} \;
```

### Docker Integration
```dockerfile
# Dockerfile z Quality Guard
FROM python:3.9
COPY quality-guard/ /usr/local/quality-guard/
RUN ln -s /usr/local/quality-guard/python-quality-wrapper.py /usr/local/bin/python
# Teraz 'python' automatycznie sprawdza jakość
```

## 🎛️ Dostosowywanie

### Własne Reguły
```python
# custom_rules.py
class CustomCodeAnalyzer(CodeAnalyzer):
    def check_business_rules(self, ast_node, file_path):
        # Twoje własne reguły biznesowe
        if self.contains_hardcoded_credentials(ast_node):
            self.violations.append({
                'type': 'HARDCODED_CREDENTIALS',
                'message': 'Znaleziono hardcoded credentials',
                'severity': 'error'
            })
```

### Integracja z IDE
```json
// .vscode/tasks.json
{
  "tasks": [
    {
      "label": "Quality Check Current File",
      "type": "shell",
      "command": "python",
      "args": ["interpreter_quality_guard.py", "${file}"],
      "group": "build",
      "presentation": {
        "reveal": "always"
      }
    }
  ]
}
```

## 📈 Metryki i Analytics

### Tracking Jakości
```bash
# Automatyczne metryki w:
~/.quality-guard/metrics.json

{
  "daily_violations": 15,
  "top_violations": [
    {"type": "FUNCTION_TOO_LONG", "count": 8},
    {"type": "FILE_TOO_LARGE", "count": 4}
  ],
  "quality_trend": "improving",
  "team_compliance": 85.5
}
```

### Dashboard Web (Bonus)
```bash
# Serwer dashboard
python -m quality_guard.dashboard

# Dostępny na: http://localhost:8080
# Pokazuje:
# - Live violations
# - Team statistics  
# - Quality trends
# - Top violators
```

## 🎯 Najlepsze Praktyki

### 1. Stopniowe Wdrożenie
```bash
# Tydzień 1: Warning mode
"strict_mode": false

# Tydzień 2: Strict mode  
"strict_mode": true

# Tydzień 3: Dodatkowe reguły
"required_docstrings": true
```

### 2. Team Onboarding
```bash
# Skrypt dla nowych developerów
./onboard-developer.sh

# Co robi:
# ✅ Instaluje Quality Guard
# ✅ Konfiguruje IDE
# ✅ Ustawia aliasy
# ✅ Pokazuje tutorial
```

### 3. Emergency Override
```bash
# W nagłych sytuacjach
QUALITY_GUARD_DISABLE=1 python main.py

# Lub
export QUALITY_GUARD_EMERGENCY=1
npm start
```

## 🛠️ Troubleshooting

### Problem: Zbyt restrykcyjne reguły
```bash
# Rozwiązanie: Dostosuj konfigurację
{
  "max_file_lines": 300,      // Zwiększ z 200
  "max_function_lines": 75,   // Zwiększ z 50
  "strict_mode": false        // Wyłącz strict mode
}
```

### Problem: Conflict z istniejącymi narzędziami
```bash
# Rozwiązanie: Selective activation
export QUALITY_GUARD_ONLY_NEW_FILES=1
# Sprawdza tylko nowe/zmienione pliki
```

### Problem: Performance impact
```bash
# Rozwiązanie: Cache results
{
  "cache_results": true,
  "cache_duration": 3600    // 1 godzina
}
```

## 🎉 Rezultaty

### Przed implementacją:
- 🔴 Średnio 50+ linii na funkcję
- 🔴 Pliki 500+ linii
- 🔴 Wysokie kompleksności
- 🔴 Brak standardów

### Po implementacji:
- 🟢 Średnio 30 linii na funkcję  
- 🟢 Pliki <200 linii
- 🟢 Kompleksność <10
- 🟢 Spójne standardy

**Efekt:** LLM i developerzy **automatycznie** produkują kod wysokiej jakości, bo system **fizycznie blokuje** uruchomienie złego kodu! 🎯