# Jupyter Kernel Setup

## Quick Setup

Run the setup script:
```bash
./setup_kernel.sh
```

This will register the uv-managed Python 3.12 environment as a Jupyter kernel.

## Manual Setup

If the script doesn't work:
```bash
uv run python -m ipykernel install --user --name crypto-analysis --display-name "Python 3.12 (crypto-analysis)"
```

## Using the Kernel

1. Open `analysis/crypto_analysis.ipynb` in your IDE
2. Click the kernel selector (top-right corner)
3. Select **"Python 3.12 (crypto-analysis)"**

### If Kernel Doesn't Appear

**Method 1: Select Python Interpreter**
- Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
- Type: "Python: Select Interpreter"
- Choose: "Enter interpreter path..."
- Paste: `/Users/justra/Python/crypto-analysis/.venv/bin/python3`

**Method 2: Restart IDE**
- Close all notebooks
- Quit the IDE completely
- Reopen and try again

## Verify Setup

Run this in a notebook cell:
```python
import sys
print("Python:", sys.executable)
print("Version:", sys.version)
```

Should show:
- Executable: `/Users/justra/Python/crypto-analysis/.venv/bin/python3`
- Version: `3.12.12`

## Troubleshooting

**Kernel not found:**
```bash
# Re-run setup
./setup_kernel.sh

# Verify kernel exists
cat ~/Library/Jupyter/kernels/crypto-analysis/kernel.json
```

**Imports failing:**
- Make sure you selected the correct kernel
- Verify Python path in the verification cell
- Try restarting the IDE
