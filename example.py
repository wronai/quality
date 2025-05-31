# 🛡️ Quality Guard - Kompletne Przykłady Użycia

## 🎯 Scenariusze Real-World

### **Scenariusz 1: Funkcja bez testów**

```python


# main.py
def process_user_data(data):
    """Przetwarza dane użytkownika"""
    return data.upper()


if __name__ == "__main__":
    result = process_user_data("hello")
    print(result)
```

** Uruchomienie: **
```bash
$ python
main.py
```

** Rezultat: **
```
🚨 QUALITY
GUARD: Kod
nie
może
być
uruchomiony
== == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
❌ MISSING_UNIT_TEST
📍 main.py: 1
🔧 Funkcja: process_user_data
📝 Funkcja
'process_user_data'
nie
ma
testów
jednostkowych
💡 Stwórz
test
w
tests / test_main.py:


def test_process_user_data():
    # Arrange
    # Act
    result = process_user_data("hello")
    # Assert
    assert result == "HELLO"

🔧 Napraw
powyższe
problemy
i
uruchom
ponownie
```

### **Scenariusz 2: Funkcja bez dokumentacji**

```python


# utils.py
def calculate_tax(amount, rate):
    return amount * rate

# Uruchomienie
$ python - c
"from utils import calculate_tax; print(calculate_tax(100, 0.2))"
```

** Rezultat: **
```
🚨 QUALITY
GUARD: Kod
nie
może
być
uruchomiony
== == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
❌ MISSING_DOCUMENTATION
📍 utils.py: 1
🔧 Funkcja: calculate_tax
📝 Funkcja
'calculate_tax'
nie
ma
wymaganej
dokumentacji(docstring)
💡 Dodaj
dokumentację
opisującą
cel, parametry
i
wartość
zwracaną:


def calculate_tax(amount, rate):
    """
    Oblicza podatek od kwoty.

    Args:
        amount: Kwota bazowa
        rate: Stawka podatkowa (0.0-1.0)

    Returns:
        Kwota podatku
    """
    return amount * rate

🔧 Napraw
powyższe
problemy
i
uruchom
ponownie
```

### **Scenariusz 3: Funkcja zbyt złożona**

```python


# complex_logic.py
def process_order(order):
    if order.status == "pending":
        if order.payment_method == "card":
            if order.amount > 1000:
                if order.customer.vip:
                    if order.items:
                        for item in order.items:
                            if item.stock > 0:
                                # ... więcej logiki
                                return "processed"
    return "failed"

# Uruchomienie
$ python
complex_logic.py
```

** Rezultat: **
```
🚨 QUALITY
GUARD: Kod
nie
może
być
uruchomiony
== == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
❌ HIGH_COMPLEXITY
📍 complex_logic.py: 1
🔧 Funkcja: process_order
📝 Funkcja
'process_order'
ma
kompleksność
15(maksimum: 10)
💡 Uprość
logikę
funkcji
lub
podziel
ją
na
mniejsze
części

❌ FUNCTION_TOO_LONG
📍 complex_logic.py: 1
🔧 Funkcja: process_order
📝 Funkcja
'process_order'
ma
75
linii(maksimum: 50)
💡 Podziel
funkcję
na
mniejsze, bardziej
specjalizowane
funkcje

🔧 Napraw
powyższe
problemy
i
uruchom
ponownie
```

## 🔧 Różne Metody Implementacji

### **Metoda 1: Dekoratory (Precyzyjne)**

```python
# service.py
from quality_guard import require_tests, require_docs, enforce_quality


@require_tests
@require_docs
def critical_function(data):
    """Krytyczna funkcja biznesowa"""
    return process_data(data)


@enforce_quality  # Wszystkie reguły
def another_function():
    """Inna funkcja"""
    pass


# Użycie - automatyczna kontrola przy wywołaniu
result = critical_function("test")  # Sprawdzi testy i docs
```

### **Metoda 2: Metaclass (Całe klasy)**

```python
# models.py
from quality_guard import QualityGuardMeta


class UserService(metaclass=QualityGuardMeta):
    """Wszystkie metody automatycznie sprawdzane"""

    def create_user(self, data):
        """Tworzy użytkownika"""
        return User(data)

    def validate_email(self, email):
        """Waliduje email"""
        return "@" in email

    def send_notification(self, user_id, message):
        """Wysyła powiadomienie"""
        pass


# Każda metoda automatycznie sprawdzana przy wywołaniu
service = UserService()
service.create_user(data)  # Automatyczna kontrola jakości
```

### **Metoda 3: Context Manager (Zakresy)**

```python
# processing.py
from quality_guard import QualityScope

with QualityScope() as scope:
    # Wszystkie funkcje w tym zakresie są sprawdzane

    def temp_function(x):
        return x * 2


    def another_temp(y):
        return y + 1


    result = temp_function(5)  # Sprawdzane
    result2 = another_temp(3)  # Sprawdzane


# Poza scope - normalne działanie
def normal_function():
    pass


normal_function()  # Nie sprawdzane
```

### **Metoda 4: Globalna Instalacja (Automatyczna)**

```python
# Na początku aplikacji lub w __init__.py
import quality_guard  # Automatycznie aktywuje dla wszystkich modułów

# Teraz wszystkie importy są sprawdzane
from my_module import my_function  # my_function automatycznie ma Quality Guard
from utils import helper_function  # helper_function automatycznie sprawdzana

# Żadnych dodatkowych dekoratorów nie trzeba!
my_function()  # Sprawdzane automatycznie
```

### **Metoda 5: Import Hook (Najbardziej elegancka)**

```python
# main.py
import quality_guard_hook  # Aktywuje hook

# Wszystkie kolejne importy mają Quality Guard
import my_services  # Automatycznie dodany Quality Guard do wszystkich funkcji
import data_processors  # Automatycznie chronione
import business_logic  # Automatycznie walidowane

# Normalne użycie - kontrola w tle
my_services.process_data("test")
data_processors.clean_data(raw_data)
business_logic.calculate_price(item)
```

## 🛠️ Konfiguracja Różnych Scenariuszy

### **Startup/Prototyp (Łagodne reguły)**

```json
{
    "require_tests": false,
    "require_docstrings": false,
    "max_function_lines": 100,
    "max_complexity": 15,
    "enforcement_level": "warning",
    "auto_generate": {
        "tests": true,
        "docs": true
    }
}
```

### **Produkcja (Rygorystyczne reguły)**

```json
{
    "require_tests": true,
    "require_docstrings": true,
    "require_architecture_docs": true,
    "max_function_lines": 30,
    "max_complexity": 7,
    "enforcement_level": "error",
    "auto_generate": {
        "tests": false,
        "docs": false
    }
}
```

### **Legacy Code (Stopniowe wdrożenie)**

```json
{
    "require_tests": false,
    "require_docstrings": true,
    "max_function_lines": 200,
    "max_complexity": 20,
    "enforcement_level": "warning",
    "legacy_mode": true,
    "whitelist_files": ["old_module.py", "legacy/*"]
}
```

## 🚀 Instalacja Różnymi Metodami

### **Super Łatwa (1 komenda)**

```bash
# Opcja 1: Pip package
pip
install
quality - guard
import quality_guard  # Gotowe!

# Opcja 2: Jeden plik
curl - O
https: // raw.githubusercontent.com / repo / setup_quality_guard.py
python
setup_quality_guard.py - -pip
```

### **Zaawansowana (Pełna kontrola)**

```bash
# Interaktywna instalacja
python
setup_quality_guard.py

# Wybierz opcję:
# 1. 📦 Pakiet pip (zalecane)
# 2. 🌍 sitecustomize.py (automatyczne)
# 3. 📁 Lokalna w projekcie
# 4. 🌿 Zmienne środowiskowe
# 5. 🪝 Import hook
# 6. 🚀 Wszystkie opcje
```

### **Enterprise (CI/CD Integration)**

```yaml
# .github/workflows/quality.yml
name: Quality
Guard
on: [push, pull_request]
jobs:
quality:
runs - on: ubuntu - latest
steps:
- uses: actions / checkout @ v3
- name: Setup
Quality
Guard
run: |
pip
install
quality - guard
quality - guard - -config
production.json
- name: Run
with Quality Control
run: |
python
main.py  # Automatycznie sprawdzane
```

## 💡 Integracja z IDE

### **VS Code Integration**

```json
//.vscode / settings.json
{
    "python.defaultInterpreterPath": "./quality_guard_python.sh",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.qualityGuardEnabled": true,
    "files.associations": {
        "*.py": "python-quality"
    }
}
```

### **PyCharm Integration**

```python
# PyCharm External Tool
# Program: python
# Arguments: -m quality_guard $FilePath$
# Working Directory: $ProjectFileDir$
```

## 📊 Monitoring i Analytics

### **Dashboard Web**

```bash
# Uruchom dashboard
python - m
quality_guard.dashboard

# Dostępny na http://localhost:8080
# Pokazuje:
# - Statystyki naruszeń
# - Top violators
# - Quality trends
# - Team compliance
```

### **Slack Integration**

```python
# slack_integration.py
from quality_guard import QualityGuardException
import slack_sdk


def quality_guard_slack_notifier(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except QualityGuardException as e:
            # Wyślij powiadomienie na Slack
            client = slack_sdk.WebClient(token=SLACK_TOKEN)
            client.chat_postMessage(
                channel="#dev-quality",
                text=f"🚨 Quality violation in {func.__name__}:\n{str(e)}"
            )
            raise

    return wrapper


```

## 🎯 Najlepsze Praktyki

### **Stopniowe Wdrożenie (3 fazy)**

```bash
# Faza 1 (Tydzień 1): Warning mode
{
    "enforcement_level": "warning",
    "require_tests": false
}

# Faza 2 (Tydzień 2): Partial enforcement
{
    "enforcement_level": "error",
    "require_tests": true,
    "require_docstrings": false
}

# Faza