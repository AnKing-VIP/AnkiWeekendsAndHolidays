from collections import defaultdict
from datetime import date
from unittest import TestCase


class TestRescheduleCards(TestCase):
    def test_best_relative_day(self):
        from src.AnkiWeekendsAndHolidays import reschedule_cards
        from src.AnkiWeekendsAndHolidays.reschedule_cards import best_due_value

        def _cards_due_on_relative_day(day):
            return [object()]

        reschedule_cards.cards_due_for_due_value = _cards_due_on_relative_day
        reschedule_cards.today_date = lambda: date(2022, 3, 13)  # a sunday
        reschedule_cards.conf = {
            "skip_dates": [],
            "skip_mon": False,
            "skip_tue": False,
            "skip_wed": False,
            "skip_thu": False,
            "skip_fri": False,
            "skip_sat": False,
            "skip_sun": True,
            "only_mature_cards": False,
            "min_interval_days": 0,
            "reschedule_direction": "both",
            "max_change_days": 30,
            "max_days_lookahead": 90,
        }

        self.assertEqual(
            best_due_value(13, 1, defaultdict(lambda: 0, {12: 1}), days_to_skip=[13]),
            14,
        )

        self.assertEqual(best_due_value(7, 1, defaultdict(lambda: 0, {6: 1})), 8)

        self.assertEqual(best_due_value(7, 1, defaultdict(lambda: 0, {8: 1})), 6)

        # the 13th is a sunday which gets skipped, then 14 through 16 is skipped so the 17th is the best candidate and 17-13=4
        reschedule_cards.conf["skip_dates"] = [["2022-03-14", "2022-03-16"]]

        self.assertTrue(best_due_value(1, 1, defaultdict(lambda: 0)) == 4)
