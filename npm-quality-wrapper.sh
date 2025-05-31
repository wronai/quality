#!/bin/bash
# npm-quality-wrapper.sh
# Wrapper dla NPM z kontrolą jakości kodu

set -e

# Kolory dla output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funkcja do wyświetlania kolorowych komunikatów
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Funkcja do sprawdzania jakości kodu
check_code_quality() {
    local project_dir=$(pwd)
    local violations=0

    print_message $BLUE "🔍 Sprawdzanie jakości kodu przed uruchomieniem NPM..."
    echo "=================================================="

    # Sprawdź czy istnieje quality-config.json
    if [[ ! -f "quality-config.json" ]]; then
        print_message $YELLOW "⚠️  Brak quality-config.json, używam domyślnych ustawień"
        create_default_config
    fi

    # Załaduj konfigurację
    local max_file_lines=$(jq -r '.max_file_lines // 200' quality-config.json 2>/dev/null || echo "200")
    local max_function_lines=$(jq -r '.max_function_lines // 50' quality-config.json 2>/dev/null || echo "50")
    local strict_mode=$(jq -r '.strict_mode // true' quality-config.json 2>/dev/null || echo "true")

    # Znajdź wszystkie pliki JS/TS
    local files=($(find src -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" 2>/dev/null))

    if [[ ${#files[@]} -eq 0 ]]; then
        print_message $GREEN "✅ Brak plików do sprawdzenia"
        return 0
    fi

    print_message $BLUE "📁 Sprawdzanie ${#files[@]} plików..."

    # Sprawdź każdy plik
    for file in "${files[@]}"; do
        local file_violations=0
        local lines=$(wc -l < "$file" 2>/dev/null || echo "0")

        # Sprawdź rozmiar pliku
        if [[ $lines -gt $max_file_lines ]]; then
            print_message $RED "  ❌ $file:0 - Plik ma $lines linii (maksimum: $max_file_lines)"
            print_message $YELLOW "     💡 Podziel plik na mniejsze moduły"
            ((violations++))
            ((file_violations++))
        fi

        # Sprawdź funkcje (prosta heurystyka dla JS/TS)
        local func_lines=0
        local in_function=false
        local func_start=0
        local brace_count=0
        local line_num=0

        while IFS= read -r line; do
            ((line_num++))

            # Wykryj początek funkcji
            if [[ $line =~ (function[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*|const[[:space:]]+[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*=[[:space:]]*\([^)]*\)[[:space:]]*=\>) ]]; then
                if [[ $in_function == false ]]; then
                    in_function=true
                    func_start=$line_num
                    func_lines=0
                    brace_count=0
                fi
            fi

            if [[ $in_function == true ]]; then
                ((func_lines++))

                # Licz nawiasy klamrowe
                local open_braces=$(echo "$line" | tr -cd '{' | wc -c)
                local close_braces=$(echo "$line" | tr -cd '}' | wc -c)
                ((brace_count += open_braces - close_braces))

                # Jeśli nawiasy się zamknęły, koniec funkcji
                if [[ $brace_count -le 0 && $open_braces -gt 0 ]]; then
                    if [[ $func_lines -gt $max_function_lines ]]; then
                        print_message $RED "  ❌ $file:$func_start - Funkcja ma $func_lines linii (maksimum: $max_function_lines)"
                        print_message $YELLOW "     💡 Podziel funkcję na mniejsze części"
                        ((violations++))
                        ((file_violations++))
                    fi
                    in_function=false
                fi
            fi