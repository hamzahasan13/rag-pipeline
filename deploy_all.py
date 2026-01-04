"""
Master Deployment Script - Run All Steps Automatically
Deploys the complete NVIDIA RAG Pipeline in one command.
"""
import subprocess
import sys


def run_step(step_number, script_name, description):
    """Run a deployment step and handle errors."""
    print("\n")
    print("=" * 80)
    print(f"STEP {step_number}: {description}")
    print("=" * 80)
    print()
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True
        )
        print()
        print(f"✅ Step {step_number} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print()
        print(f"❌ Step {step_number} failed!")
        print(f"Error in {script_name}")
        print("\nTroubleshooting:")
        print(f"  - Check the error messages above")
        print(f"  - You can run this step individually: python {script_name}")
        print(f"  - View logs if Docker-related: docker logs <container_name>")
        return False
    except FileNotFoundError:
        print(f"❌ Script not found: {script_name}")
        print("Make sure all deployment scripts are in the current directory.")
        return False


def main():
    """Run all deployment steps in order."""
    print("=" * 80)
    print("NVIDIA RAG PIPELINE - AUTOMATED DEPLOYMENT")
    print("=" * 80)
    print()
    print("This script will deploy the complete RAG pipeline:")
    print("  1. Check prerequisites (Docker, Git, API key)")
    print("  2. Configure environment variables")
    print("  3. Deploy vector database (Milvus)")
    print("  4. Deploy ingestion services")
    print("  5. Deploy RAG query services")
    print("  6. Verify all containers are running")
    print()
    print("Total estimated time: 10-15 minutes (first run)")
    print()
    
    # Ask for confirmation
    response = input("Continue with deployment? [y/N]: ")
    if response.lower() not in ['y', 'yes']:
        print("Deployment cancelled.")
        sys.exit(0)
    
    # Define deployment steps
    steps = [
        (1, "00_setup_prerequisites.py", "Setup Prerequisites"),
        (2, "01_configure_environment.py", "Configure Environment"),
        (3, "02_deploy_vectordb.py", "Deploy Vector Database"),
        (4, "03_deploy_ingestor.py", "Deploy Ingestion Services"),
        (5, "04_deploy_rag_services.py", "Deploy RAG Services"),
        (6, "05_verify_deployment.py", "Verify Deployment")
    ]
    
    # Run each step
    for step_num, script, description in steps:
        success = run_step(step_num, script, description)
        if not success:
            print()
            print("=" * 80)
            print("❌ DEPLOYMENT FAILED")
            print("=" * 80)
            print(f"\nFailed at Step {step_num}: {description}")
            print(f"\nTo retry from this step, run: python {script}")
            print("\nTo start over, run: python deploy_all.py")
            sys.exit(1)
    
    # All steps completed
    print()
    print("=" * 80)
    print("✅ DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print("🎉 Your NVIDIA RAG Pipeline is ready!")
    print()
    print("Next steps:")
    print("  1. Open RAG Playground: http://localhost:8090")
    print("  2. Test the API: http://localhost:8081/v1/health")
    print()
    print("Useful commands:")
    print("  - View all containers: docker ps")
    print("  - View container logs: docker logs <container_name>")
    print("  - Stop all services: docker compose -f rag/deploy/compose/vectordb.yaml down")
    print()


if __name__ == "__main__":
    main()