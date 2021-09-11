from AnkiWeekendsAndHolidays.ankiaddonconfig import window
from AnkiWeekendsAndHolidays.consts import WEEKDAYS_SHORT_NAMES
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QSpacerItem, QWidget
from .ankiaddonconfig import ConfigManager, ConfigWindow
from .gui.anking_widgets import AnkingIconsLayout, AnkiPalaceLayout

conf = ConfigManager()


def general_tab(conf_window: ConfigWindow) -> None:

    tab = conf_window.add_tab("General")

    tab.text("Move cards away from this days:", bold=True)
    tab.weekdays = tab.hlayout()
    for d in WEEKDAYS_SHORT_NAMES:
        tab.weekdays.checkbox('skip_' + d, d.capitalize())
    tab.addSpacerItem(QSpacerItem(0, 20))

    hlayout = tab.hlayout()
    only_mature_cards_cb = hlayout.checkbox(
        "only_mature_cards", "only move mature cards")

    hlayout.addSpacerItem(QSpacerItem(18, 0))
    min_interval_input = hlayout.number_input(
        "min_interval_days",
        description="minimum interval",
        tooltip="cards with intervals shorter than that many days will not get moved\n(cards with intervals >= 21 days are mature)",
        minimum=0,
        precision=1
    )

    def toggle_min_interval_input():
        if only_mature_cards_cb.isChecked():
            min_interval_input.setDisabled(True)
        else:
            min_interval_input.setDisabled(False)

    only_mature_cards_cb.clicked.connect(lambda _: toggle_min_interval_input())
    toggle_min_interval_input()

    tab.addSpacerItem(QSpacerItem(0, 15))

    tab.checkbox("execute_at_startup", "reschedule cards on startup")
    tab.addSpacerItem(QSpacerItem(0, 15))
    
    tab.text("You can disable this add-on for specific decks in the deck options")

    tab.stretch()


def add_anking_header(conf_window):
    conf_window.verticalLayout = QtWidgets.QVBoxLayout()
    conf_window.verticalLayout.setSizeConstraint(
        QtWidgets.QLayout.SetDefaultConstraint)
    conf_window.verticalLayout.setSpacing(6)
    conf_window.verticalLayout.setObjectName("verticalLayout")
    result = QtWidgets.QWidget(conf_window)
    sizePolicy = QtWidgets.QSizePolicy(
        QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(result.sizePolicy().hasHeightForWidth())
    result.setSizePolicy(sizePolicy)
    result.setMinimumSize(QtCore.QSize(0, 50))
    result.setObjectName("AnkingHeader")

    result = QWidget(conf_window)
    conf_window.verticalLayout.addWidget(result)

    conf_window.outer_layout.insertLayout(0, conf_window.verticalLayout, 0)
    return result


def add_ankipalace(conf_window):
    conf_window.horizontalLayout = QtWidgets.QHBoxLayout()
    conf_window.horizontalLayout.setSizeConstraint(
        QtWidgets.QLayout.SetFixedSize)
    conf_window.horizontalLayout.setSpacing(0)
    conf_window.horizontalLayout.setObjectName("horizontalLayout")
    result = QtWidgets.QWidget(conf_window)
    result.setEnabled(True)
    sizePolicy = QtWidgets.QSizePolicy(
        QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(result.sizePolicy().hasHeightForWidth())
    result.setSizePolicy(sizePolicy)
    result.setMinimumSize(QtCore.QSize(0, 0))
    result.setMaximumSize(QtCore.QSize(16777215, 16777215))
    result.setObjectName("AnkiPalace")
    conf_window.horizontalLayout.addWidget(result)
    conf_window.outer_layout.insertLayout(2, conf_window.horizontalLayout)

    return result


def add_anking_elements(window):
    window.AnkingHeader = add_anking_header(window)
    AnkingIconsLayout(window.AnkingHeader)

    window.AnkiPalace = add_ankipalace(window)
    AnkiPalaceLayout(window.AnkiPalace)


def setup_config():
    conf.on_window_open(add_anking_elements)

    conf.use_custom_window()

    conf.add_config_tab(general_tab)
