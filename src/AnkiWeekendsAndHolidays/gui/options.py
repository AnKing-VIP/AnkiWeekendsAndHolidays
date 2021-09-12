from aqt import mw
from aqt.qt import *

from ..consts import PLATFORM
from .anking_widgets import AnkingIconsLayout, AnkiPalaceLayout
from .forms.anki21 import options as qtform_options


class Options(QDialog):

    def __init__(self, parent=None, **kwargs):
        QDialog.__init__(self, mw, Qt.Window)
        self.parent = parent or mw
        self.mw = mw
        self.form = qtform_options.Ui_Dialog()
        self.form.setupUi(self)
        self._setupUI()
        self.exec_()

    def _setupUI(self):
        AnkingIconsLayout(self.form.AnkingHeader)
        AnkiPalaceLayout(self.form.AnkiPalace)

        # manually adjust title label font sizes on Windows
        # gap between default windows font sizes and sizes that work well
        # on Linux and macOS is simply too big
        # TODO: find a better solution
        if PLATFORM == "win":
            default_size = QApplication.font().pointSize()
            for label in [self.form.fmtLabContrib, self.form.labHeading]:
                font = label.font()
                font.setPointSize(int(default_size * 1.5))
                label.setFont(font)

