from aqt import gui_hooks, mw

from .compat import setup_compat_aliases
from .config import conf, setup_config
from .deckoptions import setup_deck_options
from .gui.menu import setup_anking_menu
from .reschedule_cards import reschedule_all_cards


def main():
    setup_deck_options()
    setup_config()
    setup_anking_menu()

    gui_hooks.profile_did_open.append(setup_compat_aliases)

    if conf['execute_on_synch']:
        gui_hooks.sync_will_start.append(reschedule_all_cards)

    if conf['execute_on_close']:
        gui_hooks.profile_will_close.append(reschedule_all_cards)


if mw is not None:
    main()
