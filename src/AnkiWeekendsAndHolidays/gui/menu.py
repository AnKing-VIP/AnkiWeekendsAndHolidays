from aqt import mw
from aqt.qt import QAction

from .anking_menu import get_anking_menu
from .options import Options


def setup_menu() -> None:
    menu = get_anking_menu()
    a = QAction("Weekends", menu)
    menu.addAction(a)
    a.triggered.connect(lambda _: Options(mw))
