## 🚀 Quick Start

### 1. Create Project and Virtual Environment
```bash
# Create project folder
mkdir nvidia-rag-project
cd nvidia-rag-project

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

You should see `(venv)` in your terminal prompt.

### 2. Install Git LFS
```bash
brew install git-lfs
git lfs install
```

### 3. Clone NVIDIA RAG Repository (Specific Version)
```bash
git clone https://github.com/NVIDIA-AI-Blueprints/rag.git && cd rag && git checkout f0af4a2 && cd ..
```

**Important:** This checks out a specific commit (`f0af4a2`) that's compatible with this course.

### 4. **CRITICAL:** Fix CPU Constraints for Low-Spec Systems

The NVIDIA repo expects 16 CPUs. Your MacBook Air has 4 cores, so you need to manually fix this:

**Edit file:** `rag/deploy/compose/docker-compose-ingestor-server.yaml`

**Find this section:**
```yaml
deploy:
  resources:
    reservations:
      cpus: '0-15'  # ← REMOVE THIS ENTIRE LINE
```

**Remove the `cpus: '0-15'` line completely.**

**Save the file.** ✅

### 5. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 6. Configure API Key

Create a `.env` file in the project root:
```
NGC_API_KEY=your_ngc_api_key_here
```

### 7. Run Deployment Scripts (In Order)

Make sure your virtual environment is activated (`(venv)` in prompt), then:
```bash
# Step 0: Setup prerequisites
python 00_setup_prerequisites.py

# Step 1: Configure environment
python 01_configure_environment.py

# Step 2: Deploy vector database
python 02_deploy_vectordb.py

# Step 3: Deploy ingestion services
python 03_deploy_ingestor.py

# Step 4: Deploy RAG services
python 04_deploy_rag_services.py

# Step 5: Verify deployment
python 05_verify_deployment.py
```

### 8. RAG Blueprint
<img width="1003" height="722" alt="image" src="https://github.com/user-attachments/assets/983454ad-48a3-475d-8bb1-c0b67636b590" />

### 9. Web UI
<img width="1470" height="738" alt="image" src="https://github.com/user-attachments/assets/9b83254c-bc80-4aac-be3a-13b137fc6162" />
