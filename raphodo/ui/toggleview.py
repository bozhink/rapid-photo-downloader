# Copyright (C) 2016-2024 Damon Lynch <damonlynch@gmail.com>

# This file is part of Rapid Photo Downloader.
#
# Rapid Photo Downloader is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Rapid Photo Downloader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Rapid Photo Downloader.  If not,
# see <http://www.gnu.org/licenses/>.

"""
Widget containing Header with Toggle Switch, and contains widget that appears or
disappears depending on the toggle switch's state.

Portions modeled on Canonical's QExpander, which is an 'Expander widget
similar to the GtkExpander', Copyright 2012 Canonical Ltd
"""

__author__ = "Damon Lynch"
__copyright__ = "Copyright 2016-2024, Damon Lynch"

from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLayout, QWidget  # noqa: F401

from raphodo.constants import DarkModeHeaderBackgroundName, HeaderBackgroundName
from raphodo.ui.panelview import QPanelView
from raphodo.ui.toggleswitch import QToggleSwitch
from raphodo.ui.viewutils import BlankWidget, is_dark_mode


class QToggleView(QPanelView):
    """
    A header bar with toggle switch over a widget that is switched on/off.
    """

    valueChanged = pyqtSignal(bool)

    def __init__(
        self,
        label: str,
        display_alternate: bool,
        object_name: str,
        toggleToolTip: str | None,
        headerColor: QColor | None = None,
        headerFontColor: QColor | None = None,
        on: bool = True,
        parent: QWidget = None,
    ) -> None:
        if headerColor is None:
            if is_dark_mode():
                headerColor = QColor(DarkModeHeaderBackgroundName)
            else:
                headerColor = QColor(HeaderBackgroundName)
        super().__init__(
            label=label,
            headerColor=headerColor,
            headerFontColor=headerFontColor,
            parent=parent,
        )
        # Override base class definition:
        self.headerLayout.setContentsMargins(5, 0, 5, 0)
        self.setObjectName(object_name)

        if display_alternate:
            self.alternateWidget = BlankWidget()
            layout = self.layout()  # type: QLayout
            layout.addWidget(self.alternateWidget)
        else:
            self.alternateWidget = None

        self.toggleSwitch = QToggleSwitch(background=headerColor, parent=self)
        self.toggleSwitch.valueChanged.connect(self.toggled)
        if toggleToolTip:
            self.toggleSwitch.setToolTip(toggleToolTip)
        self.addHeaderWidget(self.toggleSwitch)
        self.toggleSwitch.setOn(on)

    def addWidget(self, widget: QWidget) -> None:
        super().addWidget(widget)
        self.toggled(0)

    def on(self) -> bool:
        """Return if widget is expanded."""

        return self.toggleSwitch.on()

    def setOn(self, isOn: bool) -> None:
        """Expand the widget or not."""

        self.toggleSwitch.setOn(isOn)

    @pyqtSlot(int)
    def toggled(self, value: int) -> None:
        if self.content is not None:
            self.content.setVisible(self.on())
            if self.alternateWidget is not None:
                self.alternateWidget.setVisible(not self.on())

        self.valueChanged.emit(self.on())

    def minimumSize(self) -> QSize:
        size = super().minimumSize()
        width = size.width()
        height = self.minimumHeight()
        return QSize(width, height)

    def minimumHeight(self) -> int:
        if not self.toggleSwitch.on():
            return self.header.height()
        else:
            # critically important to call updateGeometry(), as minimum height is
            # recalculated *after* sizeHint has been called by the Qt layout manager
            self.updateGeometry()
            return super().minimumSize().height()

    def sizeHint(self) -> QSize:
        return self.minimumSize()
