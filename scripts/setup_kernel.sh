#!/bin/bash
# Setup Jupyter kernel to use uv Python 3.12

cd "$(dirname "$0")"

echo "Setting up Jupyter kernel for crypto-analysis..."
echo ""

# Get the Python executable from uv
PYTHON_EXEC=$(uv run python -c "import sys; print(sys.executable)")
PYTHON_VERSION=$(uv run python --version)

echo "Python executable: $PYTHON_EXEC"
echo "Python version: $PYTHON_VERSION"
echo ""

# Remove old kernel if it exists
echo "Removing old kernel (if exists)..."
jupyter kernelspec remove crypto-analysis -f 2>/dev/null || true

# Install kernel using uv
echo "Installing kernel with uv Python..."
uv run python -m ipykernel install --user --name crypto-analysis --display-name "Python 3.12 (crypto-analysis)"

echo ""
echo "✓ Kernel installed successfully!"
echo ""
echo "To use in your notebook:"
echo "  1. Open analysis/crypto_analysis.ipynb in your IDE"
echo "  2. Select kernel: 'Python 3.12 (crypto-analysis)'"
echo "  3. If not visible, use: Python: Select Interpreter → Enter path:"
echo "     $PYTHON_EXEC"
echo ""

