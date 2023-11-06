from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QWidget,
)

from PyQt5.QtCore import pyqtSignal


class FocusNotifyingLineEdit(QLineEdit):
    focused_in = pyqtSignal()

    def focusInEvent(self, event):
        self.focused_in.emit()
        super(FocusNotifyingLineEdit, self).focusInEvent(event)


class GraphRequester(QWidget):
    LineEditGraf: FocusNotifyingLineEdit
    LineEditX: FocusNotifyingLineEdit
    LineEditY: FocusNotifyingLineEdit

    def __init__(self, nomer_grafika=1):
        super().__init__()
        layout = QVBoxLayout(self)
        layout_x = QHBoxLayout()
        layout_y = QHBoxLayout()
        layout_close_and_name = QHBoxLayout()
        self.LineEditGraf = FocusNotifyingLineEdit(f"график {nomer_grafika}")
        NameX = QLabel("X")
        NameY = QLabel("Y")
        Name_Close = QPushButton("x")

        self.LineEditX = FocusNotifyingLineEdit()
        self.LineEditY = FocusNotifyingLineEdit()

        layout_x.addWidget(NameX)
        layout_x.addWidget(self.LineEditX)

        layout_y.addWidget(NameY)
        layout_y.addWidget(self.LineEditY)

        Name_Close.clicked.connect(lambda: self.setParent(None))

        layout_close_and_name.addWidget(self.LineEditGraf)
        layout_close_and_name.addWidget(Name_Close)

        layout.addLayout(layout_close_and_name)  # Вложения названия и закрыть
        layout.addLayout(layout_y)  # Вложение
        layout.addLayout(layout_x)  # Вложение

        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch(1)
