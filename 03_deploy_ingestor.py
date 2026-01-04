"""
Step 3: Deploy Document Ingestion Services
- Pull ingestion service Docker images
- Start document processing services
"""
import os
from dotenv import load_dotenv
from utils.docker_helpers import docker_compose_pull, docker_compose_up, show_running_containers


def deploy_ingestor_services():
    """Deploy document ingestion and processing services."""
    compose_file = "rag/deploy/compose/docker-compose-ingestor-server.yaml"
    
    print("=" * 80)
    print("NVIDIA RAG Pipeline - Deploy Ingestion Services")
    print("=" * 80)
    print()
    
    # Load environment
    load_dotenv()
    
    # Pull images
    docker_compose_pull(compose_file, "Ingestor Services")
    print()
    
    # Start services
    docker_compose_up(compose_file, "Ingestor Services")
    print()
    
    # Show running containers
    show_running_containers()
    
    print()
    print("=" * 80)
    print("✅ Ingestion services deployed successfully!")
    print("=" * 80)
    print("\nExpected new containers:")
    print("  - compose-nv-ingest-ms-runtime-1 (Document Processor)")
    print("  - ingestor-server (Ingestion API)")
    print("  - compose-redis-1 (Cache/Queue)")
    print("\nNext step: Run 'python 04_deploy_rag_services.py'")


if __name__ == "__main__":
    deploy_ingestor_services()