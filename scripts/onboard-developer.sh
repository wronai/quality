#!/bin/bash
# onboard-developer.sh
# Interactive developer onboarding script for Quality Guard

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
QUALITY_GUARD_REPO="https://github.com/quality-guard/quality-guard.git"
DEMO_PROJECT_DIR="quality-guard-demo"
ONBOARDING_LOG="onboarding-$(date +%Y%m%d_%H%M%S).log"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$ONBOARDING_LOG"
}

# Print colored message
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}" | tee -a "$ONBOARDING_LOG"
}

# Print header
print_header() {
    local title=$1
    echo ""
    print_message $CYAN "╔══════════════════════════════════════════════════════════════╗"
    print_message $CYAN "║$(printf '%62s' "$title" | sed 's/ /·/g' | sed 's/·/ /30')║"
    print_message $CYAN "╚══════════════════════════════════════════════════════════════╝"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    print_header "🔍 CHECKING PREREQUISITES"

    local missing_tools=()

    # Check Python
    if command -v python3 >/dev/null 2>&1; then
        local python_version=$(python3 --version | cut -d' ' -f2)
        print_message $GREEN "✅ Python 3 installed: $python_version"
    else
        print_message $RED "❌ Python 3 not found"
        missing_tools+=("python3")
    fi

    # Check Git
    if command -v git >/dev/null 2>&1; then
        local git_version=$(git --version | cut -d' ' -f3)
        print_message $GREEN "✅ Git installed: $git_version"
    else
        print_message $RED "❌ Git not found"
        missing_tools+=("git")
    fi

    # Check Node.js (optional)
    if command -v node >/dev/null 2>&1; then
        local node_version=$(node --version)
        print_message $GREEN "✅ Node.js installed: $node_version"
    else
        print_message $YELLOW "⚠️ Node.js not found (optional for JS/TS projects)"
    fi

    # Check curl
    if command -v curl >/dev/null 2>&1; then
        print_message $GREEN "✅ curl available"
    else
        print_message $RED "❌ curl not found"
        missing_tools+=("curl")
    fi

    if [ ${#missing_tools[@]} -gt 0 ]; then
        print_message $RED "❌ Missing required tools: ${missing_tools[*]}"
        print_message $YELLOW "Please install missing tools and run this script again"
        exit 1
    fi

    print_message $GREEN "🎉 All prerequisites satisfied!"
}

# Get developer information
get_developer_info() {
    print_header "👨‍💻 DEVELOPER INFORMATION"

    echo "Let's get to know you better..."
    echo ""

    read -p "Your name: " DEVELOPER_NAME
    read -p "Your email: " DEVELOPER_EMAIL
    read -p "Primary programming language (python/javascript/both): " PRIMARY_LANG
    read -p "Experience level (beginner/intermediate/advanced): " EXPERIENCE_LEVEL
    read -p "Team size (1-5/6-20/20+): " TEAM_SIZE

    # Validate inputs
    DEVELOPER_NAME=${DEVELOPER_NAME:-"Anonymous Developer"}
    DEVELOPER_EMAIL=${DEVELOPER_EMAIL:-"dev@example.com"}
    PRIMARY_LANG=${PRIMARY_LANG:-"python"}
    EXPERIENCE_LEVEL=${EXPERIENCE_LEVEL:-"intermediate"}
    TEAM_SIZE=${TEAM_SIZE:-"1-5"}

    print_message $BLUE "📝 Developer Profile:"
    print_message $NC "   Name: $DEVELOPER_NAME"
    print_message $NC "   Email: $DEVELOPER_EMAIL"
    print_message $NC "   Primary Language: $PRIMARY_LANG"
    print_message $NC "   Experience: $EXPERIENCE_LEVEL"
    print_message $NC "   Team Size: $TEAM_SIZE"
}

# Install Quality Guard
install_quality_guard() {
    print_header "📦 INSTALLING QUALITY GUARD"

    print_message $BLUE "Downloading Quality Guard..."

    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"

    # Download essential files
    local base_url="https://raw.githubusercontent.com/quality-