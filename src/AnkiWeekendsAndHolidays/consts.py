from anki import version as anki_version
from anki.utils import isMac, isWin

ANKI_VERSION_TUPLE = tuple(int(i) for i in anki_version.split("."))
PLATFORM = "win" if isWin else "mac" if isMac else "lin"
