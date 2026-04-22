Meistens fehlt der grüne Play-Button aus genau einem dieser Gründe:

Er hat den falschen Ordner geöffnet.
Wenn er nur den Unterordner my_project öffnet, wird die Debug-Konfiguration aus launch.json eventuell nicht gefunden.
Er soll den Repo-Root öffnen: Der-bescht-Grundwassersimulator-vor-Welt.

Die Datei launch.json ist bei ihm nicht vorhanden.
Dann sieht man keine fertige Run-Konfiguration.
Lösung: Neueste Änderungen pullen.

Python-Extension in VS Code fehlt oder ist deaktiviert.
Ohne Python + Debugpy erscheinen die Python-Debug-Optionen nicht korrekt.

Kein Interpreter ausgewählt.
In VS Code: Command Palette → Python: Select Interpreter.

Workspace ist nicht trusted.
Bei Restricted Mode werden Features teils ausgeblendet.

Schnell-Fix für deinen Kollegen (2 Minuten):

Repo neu klonen oder git pull.
Sicherstellen, dass launch.json vorhanden ist.
VS Code neu starten.
Python-Extension aktivieren.
Interpreter wählen.
Run and Debug öffnen und Konfiguration Run Groundwater Streamlit App wählen.
Wenn du willst, kann ich dir als Nächstes eine Mini-Checkliste schicken, die du ihm 1:1 auf WhatsApp schicken kannst.

GPT-5.3-Codex • 0.9x