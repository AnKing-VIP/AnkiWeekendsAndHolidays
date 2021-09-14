import datetime

from aqt import mw
from aqt.utils import tooltip

from .config import conf
from .consts import ANKI_VERSION_TUPLE, WEEKDAYS_SHORT_NAMES


def today_date():
    return datetime.datetime.fromtimestamp(
        mw.col.crt + mw.col.sched.today*86400).date()


def due_to_date(due):
    # global datetime
    return today_date() + datetime.timedelta(days=due)


def dues_to_skip_relative():
    res = set()
    for t in range(conf['max_days_lookahead']):
        if due_to_date(t).weekday() in weekdays_to_skip():
            res.add(t)
        elif due_to_date(t).isoformat() in conf['skip_dates']:
            res.add(t)
    return list(res)


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


def _possible_relative_days(day, max_diff, days_to_skip):
    min_day = max(day - max_diff, 0)
    max_day = day + max_diff
    return filter(lambda x: x not in days_to_skip, range(min_day, max_day+1))


def best_relative_day(day, ivl, num_cards_due_on_day, days_to_skip=None):
    days_to_skip = days_to_skip or dues_to_skip_relative()

    cur_diff = int(0.1 * ivl)
    while True:
        possible_relative_days = _possible_relative_days(
            day, cur_diff, days_to_skip)
        if possible_relative_days:
            possible_relative_days = sorted(
                possible_relative_days, key=lambda x: abs(x - day))
            return min(possible_relative_days, key=lambda x: num_cards_due_on_day[x])

        cur_diff += max(int(0.05 * ivl), 1)

        if cur_diff >= conf.get("max_change_days"):
            return None


def cards_due_on_relative_day(day):
    return mw.col.find_cards(f'prop:due={day}')


def reschedule_card(card, undo_entry_id, num_cards_due_on_day, days_to_skip=None):

    if mw.col.decks.config_dict_for_deck_id(card.current_deck_id()).get('weekends_disabled'):
        return False

    # Anki considers cards with intervals greater than 21 days as mature
    if conf["only_mature_cards"] and card.ivl < 21:
        return False

    if card.ivl < conf["min_interval_days"]:
        return False

    relative_due = card.due - mw.col.sched.today
    try:
        best_relative_due = best_relative_day(
            relative_due, card.ivl, num_cards_due_on_day, days_to_skip)
    # ValueError when no possible date to reschedule,
    # then leave at original due date.
    except ValueError:
        return False

    if best_relative_due is None:
        return False

    due = best_relative_due + mw.col.sched.today
    card.due = due

    num_cards_due_on_day[best_relative_due] += 1

    if ANKI_VERSION_TUPLE >= (2, 1, 45):
        mw.col.update_card(card)
        mw.col.merge_undo_entries(undo_entry_id)
    else:
        card.flush()

    return True


class CardsDueOnRelativeDayDict(dict):

    def __missing__(self, key):
        res = self[key] = len(cards_due_on_relative_day(key))
        return res


def reschedule_all_cards():

    # if anki version is >= 2.1.45, the new undo system is used and the old otherwise
    if ANKI_VERSION_TUPLE >= (2, 1, 45):
        undo_entry_id = mw.col.add_custom_undo_entry("Rescheduling")
    else:
        mw.checkpoint("Reschedule")

    # using this instead of calling len(card(due_on_relative_day(day))) everytime because that is slow
    num_cards_due_on_day = CardsDueOnRelativeDayDict()

    days_to_skip = dues_to_skip_relative()
    card_ids = cards_to_reschedule()
    cards = [mw.col.get_card(cid) for cid in card_ids]
    cnt = 0
    mw.progress.start(label="Rescheduling...")
    for i, card in enumerate(cards):
        if reschedule_card(card, undo_entry_id, num_cards_due_on_day, days_to_skip):
            cnt += 1

        mw.progress.update(value=i, max=len(cards))
        mw.app.processEvents()

        if mw.progress.want_cancel():
            mw.progress.finish()
            if ANKI_VERSION_TUPLE >= (2, 1, 45):
                mw.col.undo()
            else:
                mw.col.undo_legacy()
            mw.reset()
            return

    if not conf.get('no_tooltip'):
        tooltip(f"Rescheduled {cnt} card(s)")

    if ANKI_VERSION_TUPLE < (2, 1, 45):
        mw.col.reset()

    mw.progress.finish()
    mw.reset()
