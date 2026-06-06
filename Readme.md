# Corporate valuation
This is to understand the working of RAG and collect the relevant data from the annual report.

## 1. Setting up the conda environment and other required codes
```sh
conda create -n cv python=3.12.0 -y -y
conda activate cv
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
import torch
print(torch.__version__)
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))

conda deactivate
conda remove -n cv --all -y -y
```
## 2. Document loading

## 3. Embedding 
Tried using the gemini initially, but had to switch due to payment restrictions

## 4. Setting up docker
```sh
docker --version

# Initiate 
docker run -d `
  --name qdrant `
  -p 6333:6333 `
  -v qdrant_storage:/qdrant/storage `
  qdrant/qdrant

# Check in http://localhost:6333/dashboard
docker ps
```


