from unittest import TestCase


class TestRescheduleCards(TestCase):

    def test_best_relative_day(self):
        from src.AnkiWeekendsAndHolidays import reschedule_cards
        from src.AnkiWeekendsAndHolidays.reschedule_cards import \
            best_relative_day

        def _cards_due_on_relative_day(day):
            return [object()]
        reschedule_cards.cards_due_on_relative_day = _cards_due_on_relative_day

        self.assertEqual(best_relative_day(12, 1, [11, 12]), 13)
        self.assertTrue(best_relative_day(12, 1, [11, 12, 13]) in [10, 14])
