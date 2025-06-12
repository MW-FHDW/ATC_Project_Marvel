Write-Host "Überprüfe, ob Python installiert ist..."
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python ist nicht installiert. Versuche, Python automatisch herunterzuladen und zu installieren..."
    $pythonInstaller = "$env:TEMP\python-installer.exe"
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe" -OutFile $pythonInstaller
    # Installiere NUR für den aktuellen User
    Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1" -Wait
    Remove-Item $pythonInstaller
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        Write-Host "Python konnte nicht automatisch installiert werden. Bitte installiere Python manuell und starte das Skript erneut."
        exit 1
    } else {
        Write-Host "Python wurde erfolgreich installiert: $($python.Source)"
    }
} else {
    Write-Host "Python ist installiert: $($python.Source)"
}

Write-Host "Überprüfe, ob pip installiert ist..."
$pip = Get-Command pip -ErrorAction SilentlyContinue
if (-not $pip) {
    Write-Host "pip ist nicht installiert. Versuche, pip automatisch zu installieren..."
    python -m ensurepip --upgrade
    $pip = Get-Command pip -ErrorAction SilentlyContinue
    if (-not $pip) {
        Write-Host "pip konnte nicht automatisch installiert werden. Bitte installiere pip manuell und starte das Skript erneut."
        exit 1
    } else {
        Write-Host "pip wurde erfolgreich installiert: $($pip.Source)"
    }
} else {
    Write-Host "pip ist installiert: $($pip.Source)"
}

Write-Host "Überprüfe und installiere benötigte Python-Pakete..."

$packages = @(
    "streamlit",
    "langchain_chroma",
    "langchain-huggingface",
    "langchain-ollama",
    "chromadb",
    "torch",
    "transformers",
    "sentence-transformers"
)

foreach ($pkg in $packages) {
    $installed = pip show $pkg 2>$null
    if (-not $installed) {
        Write-Host "$pkg wird installiert (nur für den aktuellen User)..."
        pip install --user $pkg
    } else {
        Write-Host "$pkg ist bereits installiert."
    }
}

# Prüfe, ob Ollama installiert ist
Write-Host "Überprüfe, ob Ollama installiert ist..."
$ollama = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollama) {
    Write-Host "Ollama ist nicht installiert. Versuche, Ollama herunterzuladen und zu installieren..."
    $ollamaInstaller = "$env:TEMP\ollama-windows.exe"
    Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile $ollamaInstaller
    Start-Process -FilePath $ollamaInstaller -Wait
    Remove-Item $ollamaInstaller
    $ollama = Get-Command ollama -ErrorAction SilentlyContinue
    if (-not $ollama) {
        Write-Host "Ollama konnte nicht automatisch installiert werden. Bitte installiere Ollama manuell und starte das Skript erneut."
        exit 1
    } else {
        Write-Host "Ollama wurde erfolgreich installiert: $($ollama.Source)"
    }
} else {
    Write-Host "Ollama ist installiert: $($ollama.Source)"
}

# Prüfe, ob das Modell llama3.2 vorhanden ist
Write-Host "Überprüfe, ob das Modell 'llama3.2' vorhanden ist..."
$models = ollama list 2>$null
if ($models -notmatch "llama3.2") {
    Write-Host "Modell 'llama3.2' wird heruntergeladen..."
    ollama pull llama3.2
} else {
    Write-Host "Modell 'llama3.2' ist bereits vorhanden."
}

cd .\PythonScripts

Write-Host "Führe SetupDB.py aus..."
python SetupDB.py

Write-Host "Starte Streamlit-App..."
streamlit run app.py