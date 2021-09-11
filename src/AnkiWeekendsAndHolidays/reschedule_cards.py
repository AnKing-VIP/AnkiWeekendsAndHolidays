
import datetime

from aqt import gui_hooks, mw
from aqt.qt import QAction, QKeySequence
from aqt.utils import showInfo, tooltip

from .compat import add_compat_aliases
from .config import conf
from .consts import ANKI_VERSION_TUPLE, WEEKDAYS_SHORT_NAMES


def today_date():
    return datetime.datetime.fromtimestamp(
        mw.col.crt + mw.col.sched.today*86400).date()


def due_to_date(due):
    # global datetime
    return today_date() + datetime.timedelta(days=due)


def dues_to_skip_relative():
    res = list()
    for t in range(conf['max_days_lookahead']):
        if due_to_date(t).weekday() in weekdays_to_skip():
            res.append(t)
        elif due_to_date(t).isoformat() in conf['dates']:
            res.append(t)
    return res


def weekdays_to_skip():
    return [
        idx
        for idx, name in enumerate(WEEKDAYS_SHORT_NAMES)
        if conf['skip_' + name] == True
    ]


def cards_to_reschedule():
    to_skip = dues_to_skip_relative()
    res = []
    for t in to_skip:
        res += cards_due_on_relative_day(t)
    return res


def _possible_relative_days(day, days_to_skip):
    max_diff = conf['max_change_days']
    min_day = day - max_diff
    max_day = day + max_diff
    res = list()
    for t in range(min_day, max_day + 1):
        if t not in days_to_skip and t >= 0:
            res.append(t)
    return res


def best_relative_day(day, days_to_skip=None):
    days_to_skip = days_to_skip or dues_to_skip_relative()
    possible_relative_days = _possible_relative_days(day, days_to_skip)
    return min(possible_relative_days, key=lambda x: len(cards_due_on_relative_day(x)))


def cards_due_on_relative_day(day):
    return mw.col.find_cards(f'prop:due={day}')


def reschedule_card(card_id, undo_entry_id, days_to_skip=None):
    card = mw.col.get_card(card_id)

    if mw.col.decks.config_dict_for_deck_id(card.current_deck_id()).get('weekends_disabled'):
        return False

    # Anki considers cards with intervals greater than 21 days as mature
    if conf["only_mature_cards"] and card.ivl < 21:
        return False

    if card.ivl < conf["min_interval_days"]:
        return False

    relative_due = card.due - mw.col.sched.today
    try:
        best_relative_due = best_relative_day(relative_due, days_to_skip)
    # ValueError when no possible date to reschedule,
    # then leave at original due date.
    except ValueError:
        return False

    due = best_relative_due + mw.col.sched.today
    card.due = due

    if ANKI_VERSION_TUPLE >= (2, 1, 45):
        mw.col.update_card(card)
        mw.col.merge_undo_entries(undo_entry_id)
    else:
        card.flush()

    return True


def reschedule_all_cards():

    # if anki version is >= 2.1.45, the new undo system is used and the old otherwise
    undo_entry_id = None
    if ANKI_VERSION_TUPLE >= (2, 1, 45):
        undo_entry_id = mw.col.add_custom_undo_entry("Rescheduling")
    else:
        mw.checkpoint("Reschedule")

    days_to_skip = dues_to_skip_relative()
    card_ids = cards_to_reschedule()
    cnt = 0
    for card_id in card_ids:
        if reschedule_card(card_id, undo_entry_id, days_to_skip):
            cnt += 1
    tooltip(f"Rescheduled {cnt} card(s)")

    if ANKI_VERSION_TUPLE < (2, 1, 45):
        mw.col.reset()
        mw.reset()


def add_menu_action():
    action = QAction("Reschedule Cards (Weekends and Holidays addon)", mw)
    action.triggered.connect(reschedule_all_cards)
    if conf['shortcut']:
        action.setShortcut(QKeySequence(conf['shortcut']))
    mw.form.menuTools.addAction(action)


def add_startup_action():
    try:
        gui_hooks.profile_did_open.append(reschedule_all_cards)
    except Exception:
        try:
            from anki.hooks import addHook
            addHook("profileLoaded", reschedule_all_cards)
        except Exception:
            showInfo("""Automatic rescheduling failed: incompatible version
                     If you see this message, please consider submitting a bug report at:
                     https://github.com/vasarmilan/AnkiWeekendsAndHolidays""")


def _main():
    add_compat_aliases()

    add_menu_action()

    if conf['execute_at_startup']:
        add_startup_action()


def main():
    gui_hooks.profile_did_open.append(_main)
