# -*- coding: utf-8 -*-
#
# Weekends and Holidays Add-on for Anki
# Copyright (C)  2022 RisingOrange
#
# This file was automatically generated by Anki Add-on Builder v1.0.0-dev.2
# It is subject to the same licensing terms as the rest of the program
# (see the LICENSE file which accompanies this program).
#
# WARNING! All changes made in this file will be lost!

"""
Initializes generated Qt forms/resources
"""

from pathlib import Path
from aqt.qt import QDir

def initialize_qt_resources():
    QDir.addSearchPath("AnKing", str(Path(__file__).parent / "AnKing"))

initialize_qt_resources()
