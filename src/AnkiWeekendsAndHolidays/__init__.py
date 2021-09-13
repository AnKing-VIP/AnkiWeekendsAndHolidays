from aqt import gui_hooks, mw
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction

from .compat import setup_compat_aliases
from .config import conf, setup_config
from .deckoptions import setup_deck_options
from .gui.menu import setup_anking_menu
from .reschedule_cards import reschedule_all_cards


def setup_tools_menu_action():
    action = QAction("Reschedule Cards (Weekends and Holidays addon)", mw)
    action.triggered.connect(reschedule_all_cards)
    if conf['shortcut']:
        action.setShortcut(QKeySequence(conf['shortcut']))
    mw.form.menuTools.addAction(action)


def main():
    setup_deck_options()
    setup_config()
    setup_anking_menu()

    gui_hooks.profile_did_open.append(setup_compat_aliases)
    gui_hooks.profile_did_open.append(setup_tools_menu_action)

    if conf['execute_at_startup']:
        gui_hooks.profile_did_open.append(reschedule_all_cards)

if mw is not None:
    main()
