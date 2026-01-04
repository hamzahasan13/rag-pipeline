"""
Step 0: Setup Prerequisites
- Verify Docker is installed and running
- Verify NVIDIA RAG repo has been cloned
- Load NGC API key from .env file
"""
import os
import subprocess
import sys
from dotenv import load_dotenv
from utils.docker_helpers import docker_login_ngc


def check_docker():
    """Verify Docker is installed and running."""
    print("Checking Docker installation...", flush=True)
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {result.stdout.strip()}", flush=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not installed or not running!", file=sys.stderr)
        print("Please install Docker Desktop: https://www.docker.com/products/docker-desktop/", file=sys.stderr)
        sys.exit(1)
    
    # Check if Docker daemon is running
    try:
        subprocess.run(
            ["docker", "ps"],
            capture_output=True,
            check=True
        )
        print("✅ Docker daemon is running", flush=True)
    except subprocess.CalledProcessError:
        print("❌ Docker daemon is not running. Please start Docker Desktop.", file=sys.stderr)
        sys.exit(1)


def check_docker_compose():
    """Verify Docker Compose is installed."""
    print("Checking Docker Compose...", flush=True)
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {result.stdout.strip()}", flush=True)
    except subprocess.CalledProcessError:
        print("❌ Docker Compose is not installed!", file=sys.stderr)
        sys.exit(1)


def check_rag_repository():
    """Verify NVIDIA RAG Blueprint repository has been cloned."""
    repo_dir = "rag"
    
    print(f"Checking for NVIDIA RAG repository at '{repo_dir}'...", flush=True)
    
    if not os.path.exists(repo_dir):
        print(f"❌ Repository not found at '{repo_dir}'!", file=sys.stderr)
        print("\nPlease clone the repository first:", file=sys.stderr)
        print("  git clone https://github.com/NVIDIA-AI-Blueprints/rag.git && cd rag && git checkout f0af4a2 && cd ..", file=sys.stderr)
        sys.exit(1)
    
    # Check if it's a valid git repository
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print(f"❌ '{repo_dir}' exists but is not a git repository!", file=sys.stderr)
        sys.exit(1)
    
    # Check for required files
    required_files = [
        'deploy/compose/vectordb.yaml',
        'deploy/compose/docker-compose-ingestor-server.yaml',
        'deploy/compose/docker-compose-rag-server.yaml'
    ]
    
    for file_path in required_files:
        full_path = os.path.join(repo_dir, file_path)
        if not os.path.exists(full_path):
            print(f"❌ Required file missing: {file_path}", file=sys.stderr)
            print("Please ensure you cloned the complete repository.", file=sys.stderr)
            sys.exit(1)
    
    print(f"✅ Repository found with all required files", flush=True)


def load_ngc_api_key():
    """Load and validate NGC API key from .env file."""
    print("Loading NGC API key from .env...", flush=True)
    
    load_dotenv()
    
    api_key = os.environ.get("NGC_API_KEY", "")
    
    if not api_key:
        print("❌ NGC_API_KEY not found in .env file!", file=sys.stderr)
        print("Please create a .env file with: NGC_API_KEY=your_key_here", file=sys.stderr)
        sys.exit(1)
    
    if not api_key.startswith("nvapi-"):
        print(f"❌ Invalid NGC API key format: {api_key[:5]}...", file=sys.stderr)
        print("NGC API keys should start with 'nvapi-'", file=sys.stderr)
        sys.exit(1)
    
    print(f"✅ NGC API key loaded: {api_key[:10]}...", flush=True)
    return api_key


def main():
    """Run all prerequisite checks and setup."""
    print("=" * 80)
    print("NVIDIA RAG Pipeline - Prerequisites Setup")
    print("=" * 80)
    print()
    
    # Step 1: Check Docker
    check_docker()
    print()
    
    # Step 2: Check Docker Compose
    check_docker_compose()
    print()
    
    # Step 3: Verify RAG repository exists
    check_rag_repository()
    print()
    
    # Step 4: Load NGC API key
    api_key = load_ngc_api_key()
    print()
    
    # Step 5: Authenticate Docker with NGC
    docker_login_ngc(api_key)
    print()
    
    print("=" * 80)
    print("✅ All prerequisites completed successfully!")
    print("=" * 80)
    print("\nNext step: Run 'python 01_configure_environment.py'")


if __name__ == "__main__":
    main()