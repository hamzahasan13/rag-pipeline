"""
Step 5: Verify Complete Deployment
- Check all 8 expected containers are running
- Display container status
"""
import subprocess
import sys


def verify_deployment():
    """Verify all RAG pipeline services are running."""
    print("=" * 80)
    print("NVIDIA RAG Pipeline - Verify Deployment")
    print("=" * 80)
    print()
    
    # Expected containers
    expected_containers = {
        "milvus-standalone": "Vector Database",
        "milvus-minio": "Object Storage",
        "milvus-etcd": "Metadata Store",
        "compose-redis-1": "Cache/Queue",
        "compose-nv-ingest-ms-runtime-1": "Document Processor",
        "ingestor-server": "Ingestion API",
        "rag-server": "RAG Query API",
        "rag-frontend": "Web UI"
    }
    
    print(f"Expected containers: {len(expected_containers)}")
    print()
    
    # Get running containers
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            check=True
        )
        running_containers = result.stdout.strip().split('\n')
        running_containers = [c for c in running_containers if c]  # Remove empty strings
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to get running containers: {e}", file=sys.stderr)
        sys.exit(1)
    
    print("Verification Results:")
    print("-" * 80)
    
    all_running = True
    for container_name, service_desc in expected_containers.items():
        if container_name in running_containers:
            print(f"✅ {container_name:40} - {service_desc}")
        else:
            print(f"❌ {container_name:40} - {service_desc} (NOT RUNNING)")
            all_running = False
    
    print("-" * 80)
    print(f"\nRunning: {len(running_containers)}/{len(expected_containers)} containers")
    print()
    
    # Show detailed status
    print("Detailed Container Status:")
    print("-" * 80)
    subprocess.run(
        ["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}"]
    )
    print("-" * 80)
    print()
    
    if all_running:
        print("=" * 80)
        print("✅ All services are running successfully!")
        print("=" * 80)
        print("\n🎉 Your RAG pipeline is ready!")
        print("\nWhat you can do now:")
        print("  1. Open RAG Playground: http://localhost:8090")
        print("  2. Test APIs programmatically (wait for Part 2 scripts)")
        print("\nUseful commands:")
        print("  - View logs: docker logs <container_name>")
        print("  - Stop all: docker compose -f rag/deploy/compose/vectordb.yaml down")
        print("             docker compose -f rag/deploy/compose/docker-compose-ingestor-server.yaml down")
        print("             docker compose -f rag/deploy/compose/docker-compose-rag-server.yaml down")
    else:
        print("=" * 80)
        print("⚠️  Some services are not running!")
        print("=" * 80)
        print("\nTroubleshooting:")
        print("  - Check logs: docker logs <container_name>")
        print("  - Restart a service: Re-run the corresponding deploy script")
        print("  - Check Docker resources: Ensure Docker has enough memory/CPU")


if __name__ == "__main__":
    verify_deployment()