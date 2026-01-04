"""
Step 2: Deploy Vector Database (Milvus)
- Pull Milvus Docker images
- Start Milvus and supporting services (MinIO, etcd)
"""
import os
from dotenv import load_dotenv
from utils.docker_helpers import docker_compose_pull, docker_compose_up, show_running_containers


def deploy_vector_database():
    """Deploy Milvus vector database and dependencies."""
    compose_file = "rag/deploy/compose/vectordb.yaml"
    
    print("=" * 80)
    print("NVIDIA RAG Pipeline - Deploy Vector Database")
    print("=" * 80)
    print()
    
    # Load environment
    load_dotenv()
    
    # Pull images
    docker_compose_pull(compose_file, "Vector Database")
    print()
    
    # Start services
    docker_compose_up(compose_file, "Vector Database")
    print()
    
    # Show running containers
    show_running_containers()
    
    print()
    print("=" * 80)
    print("✅ Vector Database deployed successfully!")
    print("=" * 80)
    print("\nExpected containers:")
    print("  - milvus-standalone (Vector Database)")
    print("  - milvus-minio (Object Storage)")
    print("  - milvus-etcd (Metadata Store)")
    print("\nNext step: Run 'python 03_deploy_ingestor.py'")


if __name__ == "__main__":
    deploy_vector_database()