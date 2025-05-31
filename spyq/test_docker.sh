#!/bin/bash
set -e

# Build the test image
echo "🚀 Building Docker image..."
docker build -t spyq-test .

# Create a test directory
TEST_DIR="/tmp/spyq_test_$(date +%s)"
mkdir -p "$TEST_DIR"

# Function to clean up
docker_cleanup() {
    echo "🧹 Cleaning up..."
    docker rm -f spyq-test-container 2>/dev/null || true
    rm -rf "$TEST_DIR"
}

# Register cleanup function
trap docker_cleanup EXIT

# Run tests in the container
echo "🔍 Running tests in Docker container..."
docker run --rm -it --name spyq-test-container \
    -v "$(pwd)":/app \
    -v "$TEST_DIR":/test \
    -w /app \
    spyq-test \
    /bin/bash -c "
        set -e
        echo '📦 Installing package in development mode...'
        pip install -e .

        echo '✅ Testing spyq --version'
        spyq --version

        echo '✅ Testing spyq version'
        spyq version

        echo '✅ Testing spyq setup in test directory'
        cd /test
        spyq setup

        echo '✅ Verifying files were created'
        ls -la

        echo '✅ Testing spyq setup --force'
        spyq setup --force

        echo '✅ All tests completed successfully!'
    "

echo "🎉 All tests passed!"

# Run the Ansible playbook
echo "🚀 Running Ansible playbook..."
ansible-playbook test_playbook.yml

echo "✅ All tests completed successfully!"
