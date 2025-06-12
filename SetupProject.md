# Wie setze ich das Projekt erstmalig auf?

1. SetupProject.ps1 ausführen
    a. Öffne PowerShell
    b. "SetupProject.ps1" eingeben und ausführen

## Was mache ich, wenn ich das PowerShell-Skript nicht ausfühen kann?

- Führe folgenden Befehl aus, um das Ausführen von PowerShell-Skripten für den aktuellen User zu erlauben:
"Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser"

## Was mache ich, wenn der Befehl "streamlit" nicht erkannt wird?
- Füge den Pfad der streamlit-Installation zur Umgebungsvariable "PATH" hinzu.
- https://learn.microsoft.com/de-de/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)