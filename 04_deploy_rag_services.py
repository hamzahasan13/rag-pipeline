"""
Step 4: Deploy RAG Query Services
- Pull RAG server Docker images
- Start RAG query API and playground UI
"""
import os
from dotenv import load_dotenv
from utils.docker_helpers import docker_compose_pull, docker_compose_up, show_running_containers


def deploy_rag_services():
    """Deploy RAG query server and playground."""
    compose_file = "rag/deploy/compose/docker-compose-rag-server.yaml"
    
    print("=" * 80)
    print("NVIDIA RAG Pipeline - Deploy RAG Services")
    print("=" * 80)
    print()
    
    # Load environment
    load_dotenv()
    
    # Pull images
    docker_compose_pull(compose_file, "RAG Services")
    print()
    
    # Start services
    docker_compose_up(compose_file, "RAG Services")
    print()
    
    # Show running containers
    show_running_containers()
    
    print()
    print("=" * 80)
    print("✅ RAG services deployed successfully!")
    print("=" * 80)
    print("\nExpected new containers:")
    print("  - rag-server (RAG Query API)")
    print("  - rag-playground (Web UI)")
    print("\nAPI Endpoints:")
    print("  - Chat: http://localhost:8081/v1/chat/completions")
    print("  - Search: http://localhost:8081/v1/search")
    print("  - Health: http://localhost:8081/v1/health")
    print("\nRAG Playground:")
    print("  - Web UI: http://localhost:8090")
    print("\nNext step: Run 'python 05_verify_deployment.py' to verify all services")


if __name__ == "__main__":
    deploy_rag_services()