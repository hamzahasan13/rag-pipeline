"""
Reusable helper functions for Docker operations.
"""
import subprocess
import sys
import os


def run_command(command, description, env=None):
    """
    Run a shell command with error handling.
    
    Args:
        command: List of command arguments
        description: Human-readable description for logging
        env: Environment variables (defaults to os.environ)
    
    Returns:
        subprocess.CompletedProcess object
    """
    if env is None:
        env = os.environ
    
    print(f"{description}...", flush=True)
    try:
        result = subprocess.run(
            command,
            env=env,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} - Success", flush=True)
        if result.stdout.strip():
            print(result.stdout, flush=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)


def docker_login_ngc(api_key):
    """Authenticate Docker with NVIDIA Container Registry."""
    print("Authenticating Docker with NGC...", flush=True)
    try:
        process = subprocess.Popen(
            ["docker", "login", "nvcr.io", "-u", "$oauthtoken", "--password-stdin"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=api_key)
        
        if process.returncode == 0:
            print("✅ Docker authenticated with NGC", flush=True)
        else:
            print(f"❌ Docker login failed: {stderr}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"❌ Docker login error: {e}", file=sys.stderr)
        sys.exit(1)


def docker_compose_pull(compose_file, service_name):
    """Pull Docker Compose images."""
    run_command(
        ["docker", "compose", "-f", compose_file, "pull", "--quiet"],
        f"Pulling {service_name} images"
    )


def docker_compose_up(compose_file, service_name):
    """Start Docker Compose services."""
    run_command(
        ["docker", "compose", "-f", compose_file, "up", "-d"],
        f"Starting {service_name} services"
    )


def show_running_containers():
    """Display all running Docker containers."""
    print("\nRunning Docker Containers:", flush=True)
    print("-" * 80, flush=True)
    subprocess.run(
        ["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}"]
    )
    print("-" * 80, flush=True)


def get_user_id():
    """Get current user ID for Docker permissions."""
    try:
        user_id = subprocess.check_output("id -u", shell=True).decode().strip()
        return user_id
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to get user ID: {e}", file=sys.stderr)
        sys.exit(1)