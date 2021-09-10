import datetime

from aqt import mw
from aqt.qt import QAction, QKeySequence
from aqt.utils import showInfo

config = mw.addonManager.getConfig(__name__)


def today_date():
    return datetime.datetime.fromtimestamp(
        mw.col.crt + mw.col.sched.today*86400).date()


def due_to_date(due):
    # global datetime
    return today_date() + datetime.timedelta(days=due)


def dues_to_skip_relative():
    res = list()
    for t in range(config['max_days_lookahead']):
        if due_to_date(t).weekday() in config['weekdays_skip']:
            res.append(t)
        elif due_to_date(t).isoformat() in config['dates']:
            res.append(t)
    return res


def cards_to_reschedule():
    to_skip = dues_to_skip_relative()
    res = []
    for t in to_skip:
        res += cards_due_on_relative_day(t)
    return res


def _possible_relative_days(day, ivl, days_to_skip):
    max_diff = int(min([
        config['max_change_days'] or 7,
        ivl*config['max_change_percent']/100
    ]))
    min_day = day - max_diff
    max_day = day + max_diff
    res = list()
    for t in range(min_day, max_day + 1):
        if t not in days_to_skip and t >= 0:
            res.append(t)
    return res


def best_relative_day(day, ivl, days_to_skip=None):
    days_to_skip = days_to_skip or dues_to_skip_relative()
    possible_relative_days = _possible_relative_days(
        day, ivl, days_to_skip)
    return min(possible_relative_days, key=cards_due_on_relative_day)


def cards_due_on_relative_day(day):
    return mw.col.find_cards(f'prop:due={day}')


def reschedule_card(card_id, days_to_skip=None):
    card = mw.col.get_card(card_id)
    relative_due = card.due - mw.col.sched.today
    try:
        best_relative_due = best_relative_day(relative_due, card.ivl,
                                              days_to_skip)
    # ValueError when no possible date to reschedule,
    # then leave at original due date.
    except ValueError:
        return False
    due = best_relative_due + mw.col.sched.today
    card.due = due
    card.flush()
    return True


def reschedule_all_cards():
    days_to_skip = dues_to_skip_relative()
    card_ids = cards_to_reschedule()
    for card_id in card_ids:
        reschedule_card(card_id, days_to_skip)
    showInfo(
        """Successfully rescheduled cards originally scheduled on unwanted days.""")


action = QAction("Reschedule Cards (Weekends and Holidays addon)", mw)
action.triggered.connect(reschedule_all_cards)
if config['shortcut']:
    action.setShortcut(QKeySequence(config['shortcut']))
mw.form.menuTools.addAction(action)


if config.get('execute_at_startup'):
    try:
        from aqt import gui_hooks
        gui_hooks.profile_did_open.append(reschedule_all_cards)
    except Exception:
        try:
            from anki.hooks import addHook
            addHook("profileLoaded", reschedule_all_cards)
        except Exception:
            showInfo("""Automatic rescheduling failed: incompatible version
                     If you see this message, please consider submitting a bug report at:
                     https://github.com/vasarmilan/AnkiWeekendsAndHolidays""")
