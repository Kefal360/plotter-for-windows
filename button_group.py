from collections.abc import Callable

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from flow_layout import FlowLayout


class ButtonGroup(QWidget):
    def __init__(
        self,
        category: str,
        full_names: dict[str, str],
        buttons_action: Callable[[str], None],
        parent=None,
    ):
        super().__init__()
        self.layout = QVBoxLayout()  # Создание основного лаяутв
        Doplayout = FlowLayout()
        label = QLabel(category)

        self.layout.addWidget(label)
        for button_name in full_names:
            button = QPushButton(button_name, self)

            button.setFixedWidth(80)
            button.setToolTip(
                full_names[button_name]
            )  # Создание подскачоки при наведении

            button.clicked.connect(
                lambda _, name=button_name: buttons_action(  # ignore checked state with _
                    name
                )
            )  # Назначение кнопочке действия

            Doplayout.addWidget(button)  # отрисовывание кнопок

        Doplayout.setContentsMargins(0, 0, 0, 0)

        self.layout.addLayout(Doplayout)

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)
