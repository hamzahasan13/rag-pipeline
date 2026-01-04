"""
Step 1: Configure Environment
- Set all environment variables for NVIDIA-hosted endpoints
- Modify YAML files to disable GPU requirements
- Configure Docker networks for local deployment
"""
import os
import sys
import yaml
import subprocess
from dotenv import load_dotenv
from utils.docker_helpers import get_user_id


def load_environment():
    """Load environment variables from .env file."""
    print("Loading environment variables...", flush=True)
    load_dotenv()
    
    if not os.environ.get("NGC_API_KEY"):
        print("❌ NGC_API_KEY not found in .env!", file=sys.stderr)
        sys.exit(1)
    
    print("✅ Environment variables loaded", flush=True)


def set_nvidia_hosted_endpoints():
    """Configure environment variables for NVIDIA-hosted endpoints."""
    print("\nConfiguring NVIDIA-hosted endpoints...", flush=True)
    
    # Get user ID for Docker permissions
    user_id = get_user_id()
    os.environ["USERID"] = user_id
    print(f"✅ USERID set to {user_id}", flush=True)
    
    # Set the endpoint URLs of the Hosted NIMs
    env_vars = {
        "APP_EMBEDDINGS_SERVERURL": "",
        "APP_LLM_SERVERURL": "",
        "APP_LLM_MODELNAME": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
        "APP_FILTEREXPRESSIONGENERATOR_MODELNAME": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
        "APP_FILTEREXPRESSIONGENERATOR_SERVERURL": "",
        "SUMMARY_LLM": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
        "APP_RANKING_SERVERURL": "",
        "SUMMARY_LLM_SERVERURL": "",
        "OCR_HTTP_ENDPOINT": "https://ai.api.nvidia.com/v1/cv/baidu/paddleocr",
        "OCR_INFER_PROTOCOL": "http",
        "OCR_MODEL_NAME": "paddle",
        "YOLOX_HTTP_ENDPOINT": "https://ai.api.nvidia.com/v1/cv/nvidia/nemoretriever-page-elements-v2",
        "YOLOX_INFER_PROTOCOL": "http",
        "YOLOX_GRAPHIC_ELEMENTS_HTTP_ENDPOINT": "https://ai.api.nvidia.com/v1/cv/nvidia/nemoretriever-graphic-elements-v1",
        "YOLOX_GRAPHIC_ELEMENTS_INFER_PROTOCOL": "http",
        "YOLOX_TABLE_STRUCTURE_HTTP_ENDPOINT": "https://ai.api.nvidia.com/v1/cv/nvidia/nemoretriever-table-structure-v1",
        "YOLOX_TABLE_STRUCTURE_INFER_PROTOCOL": "http",
        "APP_QUERYREWRITER_SERVERURL": "",
        "APP_QUERYREWRITER_MODELNAME": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
        "APP_VECTORSTORE_ENABLEGPUSEARCH": "False",
        "APP_VECTORSTORE_ENABLEGPUINDEX": "False",
        "ENABLE_RERANKER": "false"
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print(f"✅ Configured {len(env_vars)} environment variables", flush=True)
    print("   - LLM Model: nvidia/llama-3.3-nemotron-super-49b-v1.5")
    print("   - GPU search/index: Disabled (CPU-only)")
    print("   - Reranker: Disabled (for faster testing)")


def disable_gpu_in_milvus():
    """Remove GPU requirements from Milvus vector database config."""
    print("\nDisabling GPU requirements in Milvus...", flush=True)
    
    file_path = 'rag/deploy/compose/vectordb.yaml'
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    # Remove GPU deployment requirements
    if 'services' in data and 'milvus' in data['services']:
        if 'deploy' in data['services']['milvus']:
            del data['services']['milvus']['deploy']
            print("✓ Removed GPU deployment requirements from Milvus")
        else:
            print("! GPU deployment key not found (already removed)")
    else:
        print("! Milvus service not found in YAML", file=sys.stderr)
        sys.exit(1)
    
    # Write back
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Updated {file_path}")


def configure_docker_networks():
    """Configure Docker networks for local deployment."""
    print("\nConfiguring Docker networks...", flush=True)
    
    # Create a custom network for all RAG services
    network_name = "nvidia-rag-network"
    
    # Check if network exists, create if not
    print(f"Creating Docker network '{network_name}'...", flush=True)
    try:
        # Try to create the network (will fail silently if it already exists)
        result = subprocess.run(
            ["docker", "network", "create", network_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ Created network '{network_name}'")
        else:
            # Network might already exist
            if "already exists" in result.stderr:
                print(f"✓ Network '{network_name}' already exists")
            else:
                print(f"⚠️  Network creation warning: {result.stderr.strip()}")
    except Exception as e:
        print(f"⚠️  Network creation error: {e}")
    
    file_paths = [
        'rag/deploy/compose/vectordb.yaml',
        'rag/deploy/compose/docker-compose-ingestor-server.yaml',
        'rag/deploy/compose/docker-compose-rag-server.yaml'
    ]
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}", file=sys.stderr)
            continue
        
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Update network configuration to use custom network
        if 'networks' in data and 'default' in data['networks']:
            data['networks']['default'] = {
                'external': True,
                'name': network_name
            }
            print(f"✓ Configured network in {os.path.basename(file_path)}")
        else:
            # Add networks section if it doesn't exist
            data['networks'] = {
                'default': {
                    'external': True,
                    'name': network_name
                }
            }
            print(f"✓ Added network configuration to {os.path.basename(file_path)}")
        
        # Write back
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Configured Docker networks to use '{network_name}'")


def main():
    """Run all configuration steps."""
    print("=" * 80)
    print("NVIDIA RAG Pipeline - Environment Configuration")
    print("=" * 80)
    print()
    
    # Step 1: Load environment
    load_environment()
    
    # Step 2: Set NVIDIA-hosted endpoints
    set_nvidia_hosted_endpoints()
    
    # Step 3: Disable GPU in Milvus
    disable_gpu_in_milvus()
    
    # Step 4: Configure Docker networks
    configure_docker_networks()
    
    print()
    print("=" * 80)
    print("✅ Environment configuration completed!")
    print("=" * 80)
    print("\nNext step: Run 'python 02_deploy_vectordb.py'")


if __name__ == "__main__":
    main()