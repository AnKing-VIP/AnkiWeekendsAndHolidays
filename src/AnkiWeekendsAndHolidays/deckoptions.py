import json
from pathlib import Path

import aqt
from anki.hooks import wrap
from aqt import deckconf, gui_hooks
from aqt.qt import *

from .consts import ANKI_VERSION_TUPLE

try:
    _fromUtf8 = QString.fromUtf8 # type: ignore
except Exception:

    def _fromUtf8(s):
        return s


def setup_deck_options():
    if ANKI_VERSION_TUPLE >= (2, 1, 45):
        setup_new_deck_options()

    setup_old_deck_options()


def setup_new_deck_options():
    dir = Path(__file__).parent / "web"

    with open(dir / "raw.html") as f:
        html = f.read()
    with open(dir / "raw.js") as f:
        script = f.read()

    def on_mount(dialog):
        dialog.web.eval(script.replace("HTML_CONTENT", json.dumps(html)))

    gui_hooks.deck_options_did_load.append(on_mount)


def setup_old_deck_options():
    aqt.forms.dconf.Ui_Dialog.setupUi = wrap(
        aqt.forms.dconf.Ui_Dialog.setupUi, setup_ui, pos="after"
    )
    deckconf.DeckConf.loadConf = wrap(
        deckconf.DeckConf.loadConf, load_conf, pos="after"
    )
    deckconf.DeckConf.saveConf = wrap(
        deckconf.DeckConf.saveConf, save_conf, pos="before"
    )


def setup_ui(self, Dialog):
    r = self.gridLayout_3.rowCount()
    gridLayout_3 = QGridLayout()

    self.DisableFW = QCheckBox(self.tab_3)
    self.DisableFW.setObjectName(_fromUtf8("DisableFW"))
    self.DisableFW.setText(
        "Disable Weekends and holidays (affects all decks in this option group)"
    )
    self.DisableFW.setDisabled(False)
    gridLayout_3.addWidget(self.DisableFW, r, 0, 1, 3)
    r += 1

    self.verticalLayout_4.insertLayout(1, gridLayout_3)


def load_conf(self):
    f = self.form
    c = self.conf
    f.DisableFW.setChecked(c.get("weekends_disabled", 0))


def save_conf(self):
    f = self.form
    c = self.conf
    c["weekends_disabled"] = int(f.DisableFW.isChecked())
