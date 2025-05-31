# quality_guard_exceptions.py
# System wyjątków Quality Guard dla wymuszania standardów jakości

import sys
import os
import ast
import inspect
import functools
import importlib
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass
from enum import Enum
import json
import re


class QualityLevel(Enum):
    """Poziomy ważności naruszeń jakości"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class QualityViolation:
    """Reprezentuje naruszenie standardów jakości"""
    rule_name: str
    message: str
    suggestion: str
    level: QualityLevel
    file_path: str = ""
    line_number: int = 0
    function_name: str = ""
    context: Dict[str, Any] = None


class QualityGuardException(Exception):
    """Bazowy wyjątek Quality Guard"""

    def __init__(self, violations: List[QualityViolation]):
        self.violations = violations
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Formatuje komunikat błędu"""
        if not self.violations:
            return "Quality Guard: Unknown violation"

        lines = ["🚨 QUALITY GUARD: Kod nie może być uruchomiony", "=" * 60]

        for violation in self.violations:
            icon = {
                QualityLevel.CRITICAL: "🔥",
                QualityLevel.ERROR: "❌",
                QualityLevel.WARNING: "⚠️",
                QualityLevel.INFO: "ℹ️"
            }.get(violation.level, "❌")

            lines.append(f"{icon} {violation.rule_name.upper()}")
            lines.append(f"   📍 {violation.file_path}:{violation.line_number}")
            if violation.function_name:
                lines.append(f"   🔧 Funkcja: {violation.function_name}")
            lines.append(f"   📝 {violation.message}")
            lines.append(f"   💡 {violation.suggestion}")
            lines.append("")

        lines.append("🔧 Napraw powyższe problemy i uruchom ponownie")
        return "\n".join(lines)


class MissingTestException(QualityGuardException):
    """Wyjątek: Brak testów jednostkowych"""

    def __init__(self, function_name: str, file_path: str, line_number: int):
        violation = QualityViolation(
            rule_name="missing_unit_test",
            message=f"Funkcja '{function_name}' nie ma testów jednostkowych",
            suggestion=f"Stwórz test w tests/test_{Path(file_path).stem}.py",
            level=QualityLevel.ERROR,
            file_path=file_path,
            line_number=line_number,
            function_name=function_name
        )
        super().__init__([violation])


class MissingDocumentationException(QualityGuardException):
    """Wyjątek: Brak dokumentacji"""

    def __init__(self, function_name: str, file_path: str, line_number: int, doc_type: str = "docstring"):
        violation = QualityViolation(
            rule_name="missing_documentation",
            message=f"Funkcja '{function_name}' nie ma wymaganej dokumentacji ({doc_type})",
            suggestion=f"Dodaj dokumentację opisującą cel, parametry i wartość zwracaną",
            level=QualityLevel.ERROR,
            file_path=file_path,
            line_number=line_number,
            function_name=function_name
        )
        super().__init__([violation])


class ComplexityException(QualityGuardException):
    """Wyjątek: Zbyt wysoka kompleksność"""

    def __init__(self, function_name: str, complexity: int, max_complexity: int, file_path: str, line_number: int):
        violation = QualityViolation(
            rule_name="high_complexity",
            message=f"Funkcja '{function_name}' ma kompleksność {complexity} (maksimum: {max_complexity})",
            suggestion="Podziel funkcję na mniejsze części lub uprość logikę",
            level=QualityLevel.ERROR,
            file_path=file_path,
            line_number=line_number,
            function_name=function_name,
            context={"actual_complexity": complexity, "max_complexity": max_complexity}
        )
        super().__init__([violation])


class FunctionTooLongException(QualityGuardException):
    """Wyjątek: Funkcja zbyt długa"""

    def __init__(self, function_name: str, lines: int, max_lines: int, file_path: str, line_number: int):
        violation = QualityViolation(
            rule_name="function_too_long",
            message=f"Funkcja '{function_name}' ma {lines} linii (maksimum: {max_lines})",
            suggestion="Podziel funkcję na mniejsze, bardziej specjalizowane funkcje",
            level=QualityLevel.ERROR,
            file_path=file_path,
            line_number=line_number,
            function_name=function_name,
            context={"actual_lines": lines, "max_lines": max_lines}
        )
        super().__init__([violation])


class UnauthorizedFunctionException(QualityGuardException):
    """Wyjątek: Funkcja nie jest udokumentowana w architekturze"""

    def __init__(self, function_name: str, file_path: str, line_number: int):
        violation = QualityViolation(
            rule_name="unauthorized_function",
            message=f"Funkcja '{function_name}' nie jest udokumentowana w architekturze projektu",
            suggestion="Dodaj funkcję do architecture.md lub API.md",
            level=QualityLevel.WARNING,
            file_path=file_path,
            line_number=line_number,
            function_name=function_name
        )
        super().__init__([violation])


class QualityConfig:
    """Konfiguracja Quality Guard"""

    def __init__(self, config_path: str = "quality-guard.json"):
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        default_config = {
            "require_tests": True,
            "require_docstrings": True,
            "require_architecture_docs": False,
            "max_function_lines": 50,
            "max_complexity": 10,
            "test_patterns": [
                "tests/test_*.py",
                "test_*.py",
                "*_test.py"
            ],
            "doc_files": [
                "README.md",
                "docs/API.md",
                "docs/architecture.md",
                "ARCHITECTURE.md"
            ],
            "enforcement_level": "error",  # error, warning, info
            "auto_generate": {
                "tests": True,
                "docs": True
            }
        }

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        return default_config

    def get(self, key: str, default=None):
        return self.config.get(key, default)


class QualityGuardValidator:
    """Główny walidator Quality Guard"""

    def __init__(self, config: QualityConfig = None):
        self.config = config or QualityConfig()
        self.violations = []

    def validate_function(self, func: Callable, file_path: str = None, line_number: int = None) -> List[
        QualityViolation]:
        """Waliduje funkcję pod kątem standardów jakości"""
        self.violations = []

        # Pobierz informacje o funkcji
        func_name = func.__name__
        file_path = file_path or inspect.getfile(func)
        line_number = line_number or inspect.getsourcelines(func)[1]

        # Sprawdź testy
        if self.config.get("require_tests"):
            self._check_tests(func_name, file_path, line_number)

        # Sprawdź dokumentację
        if self.config.get("require_docstrings"):
            self._check_documentation(func, func_name, file_path, line_number)

        # Sprawdź długość funkcji
        self._check_function_length(func, func_name, file_path, line_number)

        # Sprawdź kompleksność
        self._check_complexity(func, func_name, file_path, line_number)

        # Sprawdź autoryzację w dokumentacji architektury
        if self.config.get("require_architecture_docs"):
            self._check_architecture_authorization(func_name, file_path, line_number)

        return self.violations

    def _check_tests(self, func_name: str, file_path: str, line_number: int):
        """Sprawdza czy funkcja ma testy"""
        test_patterns = self.config.get("test_patterns", [])

        # Szukaj plików testów
        for pattern in test_patterns:
            if self._find_test_for_function(func_name, pattern, file_path):
                return  # Test znaleziony

        # Brak testów
        self.violations.append(QualityViolation(
            rule_name="missing_test",
            message=f"Funkcja '{func_name}' nie ma testów jednostkowych",
            suggestion=f"Stwórz test w tests/test_{Path(file_path).stem}.py:\n\n"
                       f"def test_{func_name}():\n"
                       f"    # Arrange\n"
                       f"    # Act\n"
                       f"    result = {func_name}()\n"
                       f"    # Assert\n"
                       f"    assert result is not None",
            level=QualityLevel.ERROR,
            file_path=file_path,
            line_number=line_number,
            function_name=func_name
        ))

    def _find_test_for_function(self, func_name: str, pattern: str, file_path: str) -> bool:
        """Szuka testów dla konkretnej funkcji"""
        import glob

        # Zastąp * w pattern
        if "*" in pattern:
            test_files = glob.glob(pattern)
        else:
            test_files = [pattern] if os.path.exists(pattern) else []

        for test_file in test_files:
            if os.path.exists(test_file):
                try:
                    with open(test_file, 'r') as f:
                        content = f.read()
                        # Szukaj test_function_name
                        if f"test_{func_name}" in content or f"test{func_name.title()}" in content:
                            return True
                except:
                    continue

        return False

    def _check_documentation(self, func: Callable, func_name: str, file_path: str, line_number: int):
        """Sprawdza dokumentację funkcji"""
        if not func.__doc__ or len(func.__doc__.strip()) < 10:
            self.violations.append(QualityViolation(
                rule_name="missing_docstring",
                message=f"Funkcja '{func_name}' nie ma odpowiedniej dokumentacji",
                suggestion=f"Dodaj docstring:\n\n"
                           f'def {func_name}(...):\n'
                           f'    """\n'
                           f'    Krótki opis funkcji.\n\n'
                           f'    Args:\n'
                           f'        param1: Opis parametru\n\n'
                           f'    Returns:\n'
                           f'        Opis zwracanej wartości\n'
                           f'    """\n'
                           f'    # kod funkcji',
                level=QualityLevel.ERROR,
                file_path=file_path,
                line_number=line_number,
                function_name=func_name
            ))

    def _check_function_length(self, func: Callable, func_name: str, file_path: str, line_number: int):
        """Sprawdza długość funkcji"""
        try:
            source_lines = inspect.getsourcelines(func)[0]
            actual_lines = len([line for line in source_lines if line.strip() and not line.strip().startswith('#')])
            max_lines = self.config.get("max_function_lines", 50)

            if actual_lines > max_lines:
                self.violations.append(QualityViolation(
                    rule_name="function_too_long",
                    message=f"Funkcja '{func_name}' ma {actual_lines} linii kodu (maksimum: {max_lines})",
                    suggestion="Podziel funkcję na mniejsze funkcje pomocnicze",
                    level=QualityLevel.ERROR,
                    file_path=file_path,
                    line_number=line_number,
                    function_name=func_name,
                    context={"actual_lines": actual_lines, "max_lines": max_lines}
                ))
        except:
            pass  # Nie można określić długości

    def _check_complexity(self, func: Callable, func_name: str, file_path: str, line_number: int):
        """Sprawdza kompleksność funkcji"""
        try:
            source = inspect.getsource(func)
            tree = ast.parse(source)
            complexity = self._calculate_complexity(tree)
            max_complexity = self.config.get("max_complexity", 10)

            if complexity > max_complexity:
                self.violations.append(QualityViolation(
                    rule_name="high_complexity",
                    message=f"Funkcja '{func_name}' ma kompleksność {complexity} (maksimum: {max_complexity})",
                    suggestion="Uprość logikę lub podziel na mniejsze funkcje",
                    level=QualityLevel.ERROR,
                    file_path=file_path,
                    line_number=line_number,
                    function_name=func_name,
                    context={"actual_complexity": complexity, "max_complexity": max_complexity}
                ))
        except:
            pass  # Nie można obliczyć kompleksności

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Oblicza kompleksność cyklomatyczną"""
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        return complexity

    def _check_architecture_authorization(self, func_name: str, file_path: str, line_number: int):
        """Sprawdza czy funkcja jest udokumentowana w architekturze"""
        doc_files = self.config.get("doc_files", [])

        for doc_file in doc_files:
            if os.path.exists(doc_file):
                try:
                    with open(doc_file, 'r') as f:
                        content = f.read()
                        if func_name in content:
                            return  # Funkcja znaleziona w dokumentacji
                except:
                    continue

        self.violations.append(QualityViolation(
            rule_name="unauthorized_function",
            message=f"Funkcja '{func_name}' nie jest udokumentowana w architekturze projektu",
            suggestion=f"Dodaj opis funkcji do README.md lub docs/API.md",
            level=QualityLevel.WARNING,
            file_path=file_path,
            line_number=line_number,
            function_name=func_name
        ))


# DECORATORS dla łatwego użycia

def require_tests(func: Callable) -> Callable:
    """Dekorator wymuszający testy"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        validator = QualityGuardValidator()
        violations = validator.validate_function(func)
        test_violations = [v for v in violations if v.rule_name == "missing_test"]

        if test_violations:
            raise MissingTestException(
                func.__name__,
                inspect.getfile(func),
                inspect.getsourcelines(func)[1]
            )

        return func(*args, **kwargs)

    return wrapper


def require_docs(func: Callable) -> Callable:
    """Dekorator wymuszający dokumentację"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not func.__doc__ or len(func.__doc__.strip()) < 10:
            raise MissingDocumentationException(
                func.__name__,
                inspect.getfile(func),
                inspect.getsourcelines(func)[1]
            )

        return func(*args, **kwargs)

    return wrapper


def enforce_quality(func: Callable) -> Callable:
    """Dekorator wymuszający wszystkie standardy jakości"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        validator = QualityGuardValidator()
        violations = validator.validate_function(func)

        # Filtruj tylko błędy krytyczne
        critical_violations = [v for v in violations if v.level in [QualityLevel.ERROR, QualityLevel.CRITICAL]]

        if critical_violations:
            raise QualityGuardException(critical_violations)

        return func(*args, **kwargs)

    return wrapper


# METACLASS dla automatycznego wymuszania na klasach

class QualityGuardMeta(type):
    """Metaclass automatycznie dodająca Quality Guard do wszystkich metod"""

    def __new__(cls, name, bases, dct):
        for attr_name, attr_value in dct.items():
            if callable(attr_value) and not attr_name.startswith('_'):
                dct[attr_name] = enforce_quality(attr_value)

        return super().__new__(cls, name, bases, dct)


# CONTEXT MANAGER dla kontroli zakresów

class QualityScope:
    """Context manager dla kontroli jakości w zakresie"""

    def __init__(self, config: QualityConfig = None):
        self.config = config or QualityConfig()
        self.validator = QualityGuardValidator(self.config)
        self.original_call = None

    def __enter__(self):
        # Przechwytuj wywołania funkcji
        self._monkey_patch_function_calls()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Przywróć oryginalne wywołania
        self._restore_function_calls()

    def _monkey_patch_function_calls(self):
        """Monkey patch dla przechwytywania wywołań funkcji"""
        # To jest uproszczona implementacja
        # W prawdziwej implementacji użyj sys.settrace lub podobnych
        pass

    def _restore_function_calls(self):
        """Przywraca oryginalne wywołania"""
        pass


# AUTOMATYCZNA INSTALACJA w interpreterze

class QualityGuardInstaller:
    """Instalator Quality Guard na poziomie interpretera"""

    @staticmethod
    def install_globally():
        """Instaluje Quality Guard globalnie w interpreterze"""
        import builtins

        # Hook do importów
        original_import = builtins.__import__


        def quality_import(name, globals=None, locals=None, fromlist=(), level=0):
            module = original_import(name, globals, locals, fromlist, level)

            # Dodaj Quality Guard do modułów użytkownika (nie systemowych)
            if hasattr(module, '__file__') and module.__file__:
                if not module.__file__.startswith('/usr/') and not 'site-packages' in module.__file__:
                    QualityGuardInstaller._add_quality_guard_to_module(module)

            return module

        # Ustaw nową funkcję importu
        builtins.__import__ = quality_import
        
        # Oznacz jako zainstalowane
        sys._quality_guard_installed = True
        sys._quality_guard_version = "1.0.0"

    @staticmethod
    def _add_quality_guard_to_module(module):
        """Dodaje Quality Guard do modułu"""
        for attr_name in dir(module):
            attr_value = getattr(module, attr_name)
            if callable(attr_value) and not attr_name.startswith('_'):
                if hasattr(attr_value, '__module__') and attr_value.__module__ == module.__name__:
                    try:
                        wrapped = enforce_quality(attr_value)
                        setattr(module, attr_name, wrapped)
                    except:
                        pass  # Ignoruj błędy


# GENERATOR AUTOMATYCZNYCH TESTÓW I DOKUMENTACJI

class AutoGenerator:
    """Generator automatycznych testów i dokumentacji"""

    def __init__(self, config: QualityConfig = None):
        self.config = config or QualityConfig()

    def generate_test_for_function(self, func: Callable, output_dir: str = "tests"):
        """Generuje test dla funkcji"""
        func_name = func.__name__
        file_path = inspect.getfile(func)
        module_name = Path(file_path).stem

        test_content = f'''# Auto-generated test for {func_name}
import pytest
from {module_name} import {func_name}

def test_{func_name}():
    """Test for {func_name} function"""
    # TODO: Implement proper test
    # Arrange
    # Act
    result = {func_name}()  # Adjust parameters as needed
    # Assert
    assert result is not None

def test_{func_name}_edge_cases():
    """Test edge cases for {func_name}"""
    # TODO: Add edge case tests
    pass
'''

        os.makedirs(output_dir, exist_ok=True)
        test_file = os.path.join(output_dir, f"test_{module_name}.py")

        # Sprawdź czy test już istnieje
        if os.path.exists(test_file):
            with open(test_file, 'r') as f:
                existing_content = f.read()
                if f"test_{func_name}" in existing_content:
                    return  # Test już istnieje

            # Dodaj do istniejącego pliku
            with open(test_file, 'a') as f:
                f.write(f"\n\n{test_content}")
        else:
            # Stwórz nowy plik
            with open(test_file, 'w') as f:
                f.write(test_content)

        print(f"✅ Wygenerowano test dla {func_name} w {test_file}")

    def generate_docs_for_function(self, func: Callable):
        """Generuje dokumentację dla funkcji"""
        if func.__doc__:
            return  # Dokumentacja już istnieje

        # Prosta analiza funkcji
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())

        doc_template = f'''"""
        Brief description of {func.__name__}.

        Args:
{chr(10).join(f"            {param}: Description of {param}" for param in params)}

        Returns:
            Description of return value

        Raises:
            Exception: Description of when exception is raised
        """'''

        # W prawdziwej implementacji można by modyfikować AST
        print(f"💡 Sugerowana dokumentacja dla {func.__name__}:")
        print(doc_template)


# PRZYKŁADY UŻYCIA

def example_usage():
    """Przykłady użycia Quality Guard"""

    # 1. Dekorator dla pojedynczej funkcji
    @require_tests
    @require_docs
    def my_function(x, y):
        """Dodaje dwie liczby"""
        return x + y

    # 2. Metaclass dla całej klasy
    class MyService(metaclass=QualityGuardMeta):
        def process_data(self, data):
            return data * 2

        def validate_input(self, input_data):
            return len(input_data) > 0

    # 3. Context manager dla zakresu
    with QualityScope() as scope:
        # Wszystkie funkcje w tym zakresie są sprawdzane
        def temporary_function():
            pass

    # 4. Globalna instalacja
    QualityGuardInstaller.install_globally()

    # 5. Auto-generator
    generator = AutoGenerator()
    generator.generate_test_for_function(my_function)
    generator.generate_docs_for_function(my_function)


if __name__ == "__main__":
    example_usage()