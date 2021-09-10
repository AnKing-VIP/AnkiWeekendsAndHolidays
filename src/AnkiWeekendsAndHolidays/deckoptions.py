import json
from pathlib import Path

from aqt import gui_hooks


def setup_deck_options():
    dir = Path(__file__).parent / 'web'

    with open(dir / "raw.html") as f:
        html = f.read()
    with open(dir / "raw.js") as f:
        script = f.read()

    def on_mount(dialog):
        dialog.web.eval(script.replace("HTML_CONTENT", json.dumps(html)))

    gui_hooks.deck_options_did_load.append(on_mount)
    