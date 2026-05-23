## Setting up CUDA
```sh
conda create -n cv python=3.10.0 -y -y
conda activate cv
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

## Check if CUDA working
```sh
python
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

## Check ollama 
```sh
ollama --version
ollama pull qwen2.5:3b
ollama run qwen2.5:3b
/exit
ollama stop qwen2.5:3b
```
Sample question: Extract Revenue, EBIT and CapEx from a financial statement.

