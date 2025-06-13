# Check if Chocolatey is installed, if not, install it
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}

# Install Python 3.11
choco install python --version=3.11.9 -y

# Install Git
choco install git -y

# Install VS Code
choco install vscode -y

# Install uv (from Astral)
Invoke-Expression (Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" -UseBasicParsing).Content

# Refresh the environment (in case uv isn't available yet)
$env:Path += ";$HOME\.cargo\bin"

# Install Python packages using uv
uv pip install numpy pandas streamlit

# Install VS Code Extensions
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension charliermarsh.ruff
code --install-extension cline.vscode-cline

Write-Output "✅ SoAI 2025 Development Environment setup completed successfully!"
