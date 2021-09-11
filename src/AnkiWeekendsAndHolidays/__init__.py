from .deckoptions import setup_deck_options
from .gui.menu import setup_menu
from .reschedule_cards import main
from .config import setup_config

setup_deck_options()
setup_config()
setup_menu()
main()
