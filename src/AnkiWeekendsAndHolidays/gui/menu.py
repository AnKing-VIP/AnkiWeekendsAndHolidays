from aqt.qt import QAction

from ..config import conf
from .anking_menu import get_anking_menu


def setup_anking_menu() -> None:
    menu = get_anking_menu()
    a = QAction("Weekends and Holidays", menu)
    menu.addAction(a)
    a.triggered.connect(conf.open_config)
