from anki.cards import Card
from aqt import mw

from .utils import add_compat_alias


def setup_compat_aliases():

    add_compat_alias(mw.col, 'get_card', 'getCard')
    add_compat_alias(
        mw.col.decks, 'config_dict_for_deck_id', 'confForDid')

    def _current_deck_id(self):
        return mw.col.decks.for_card_ids([self.id])[0]
    Card.current_deck_id = _current_deck_id
