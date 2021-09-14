import datetime
from aqt import mw, Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDateEdit, QFormLayout, QFrame, QHBoxLayout, QPushButton, QScrollArea, QSpacerItem, QWidget

from .ankiaddonconfig import ConfigManager, ConfigWindow
from .consts import WEEKDAYS_SHORT_NAMES
from .gui.anking_widgets import AnkingIconsLayout, AnkiPalaceLayout

if mw is not None:
    conf = ConfigManager()
else:
    conf = None


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

    tab.checkbox("execute_on_synch", "reschedule cards before synching")
    tab.addSpacerItem(QSpacerItem(0, 15))

    tab.checkbox("execute_on_close", "reschedule cards when closing Anki")
    tab.addSpacerItem(QSpacerItem(0, 15))

    tab.text(
        "<i>You can disable this add-on for specific decks in the deck options</i>", html=True)
    tab.addSpacerItem(QSpacerItem(0, 15))

    def _reschedule_cards():

        # importing here to prevent circular import
        from .reschedule_cards import reschedule_all_cards
        reschedule_all_cards()
    tab.reschedule_button = QPushButton("Reschedule cards")
    tab.reschedule_button.clicked.connect(_reschedule_cards)
    tab.addWidget(tab.reschedule_button)
    tab.text(
        "<i>Rescheduling is undoable (Edit->Undo Rescheduling)", html=True)

    tab.stretch()


def dates_tab(conf_window):
    tab = conf_window.add_tab("Holidays")

    tab.text("Specify start and end dates for times you want to move cards away from")

    dates_layout, scroll = setup_dates_layout(conf_window)
    tab.addWidget(scroll)

    dates_layout.rows = []

    def update_skip_dates_config():
        dates = []
        for row in dates_layout.rows:
            if row.start_edit.date() == row.end_edit.date():
                dates.append(row.start_edit.date().toString(format=Qt.ISODate))
            else:
                dates.append([
                    row.start_edit.date().toString(format=Qt.ISODate),
                    row.end_edit.date().toString(format=Qt.ISODate)
                ])
        conf.set("skip_dates", dates)

    def update_dates_view():

        for row in dates_layout.rows:
            remove_row_from_ui(row)
        dates_layout.rows = []

        for date_info in conf.get("skip_dates"):
            row = QHBoxLayout()

            if isinstance(date_info, list):
                start_date_str, end_date_str = date_info
            else:
                start_date_str, end_date_str = date_info, date_info

            row.start_edit = QDateEdit(
                date=datetime.date.fromisoformat(start_date_str))
            row.end_edit = QDateEdit(
                date=datetime.date.fromisoformat(end_date_str))

            row.end_edit.setMinimumDate(row.start_edit.date())

            row.start_edit.setCalendarPopup(True)
            row.end_edit.setCalendarPopup(True)

            def on_start_date_changed(row):
                row.end_edit.setMinimumDate(row.start_edit.date())
                update_skip_dates_config()
            row.start_edit.dateChanged.connect(
                lambda *_, row=row: on_start_date_changed(row))
            row.addWidget(row.start_edit)

            row.end_edit.dateChanged.connect(update_skip_dates_config)
            row.addWidget(row.end_edit)

            def on_delete_button_click(row):
                remove_row_from_ui(row)
                dates_layout.rows.remove(row)
                update_skip_dates_config()
                update_dates_view()

            row.delete_button = QPushButton(text="X")
            row.delete_button.setFixedSize(18, 18)
            row.delete_button.clicked.connect(
                lambda _, row=row: on_delete_button_click(row))
            row.addWidget(row.delete_button)

            dates_layout.rows.append(row)
            dates_layout.addRow(row)

    def on_add_button_click():
        skip_dates = conf.get("skip_dates")
        skip_dates.append(str(datetime.date.today()))
        update_dates_view()

    def remove_row_from_ui(row):
        deleteItemsOfLayout(row)
        dates_layout.removeItem(row)

    update_dates_view()

    dates_layout.add_button = QPushButton(text="Add")
    dates_layout.add_button.clicked.connect(on_add_button_click)
    tab.addWidget(dates_layout.add_button)


def setup_dates_layout(conf_window):
    dates_layout = QFormLayout()
    inner_widget = QWidget()
    inner_widget.setLayout(dates_layout)
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.NoFrame)
    scroll.setWidget(inner_widget)
    return dates_layout, scroll


def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())


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
    conf.add_config_tab(dates_tab)
