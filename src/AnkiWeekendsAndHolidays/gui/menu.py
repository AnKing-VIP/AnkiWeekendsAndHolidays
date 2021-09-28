from aqt.qt import QAction

from ..config import conf
from .anking_menu import get_anking_menu


def setup_anking_menu() -> None:
    menu = get_anking_menu()
    action_text = "Weekends and Holidays"
    if not any([child.text() == action_text for child in menu.findChildren(QAction)]):
        a = QAction(action_text, menu)
        menu.addAction(a)
        a.triggered.connect(conf.open_config)
