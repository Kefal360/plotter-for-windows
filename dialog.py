from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QScrollArea,
    QWidget,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QHBoxLayout,
    QCheckBox,
)

import numpy as np

from button_group import ButtonGroup
from constants_plotter_dialog import FUNCTION_NAMES
from graph_requester import GraphRequester
from utils import size

from expr_parser import Parser

from graph_widget import GraphWidget


class PlotterDialog(QDialog):
    focused_line_edit = None

    def __init__(
        self,
        variable_values: dict[str, np.ndarray] = {},
        variable_full_names: dict[str, str] = {},
        function_full_names: dict[str, str] = FUNCTION_NAMES,
    ):
        super().__init__()

        self.variable_values = variable_values

        self.setWindowTitle("Графопостроитель")

        layout_boss = QVBoxLayout()  # главный лояут

        self.scroll = QScrollArea()

        self.scroll.verticalScrollBar().rangeChanged.connect(self.scroll_bottom)

        scrollWidget = QWidget()

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.inputs_layout = QVBoxLayout()  # лаяут первой трети
        self.inputs_layout.addStretch(1)

        self.num_of_input = 0  # инициализация первого графика
        self.add_input()

        QTimer.singleShot(0, self.focus_first_input)

        scrollWidget.setLayout(self.inputs_layout)

        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(scrollWidget)

        layout_boss.addWidget(self.scroll)

        Button_make_fun_button = QPushButton("+")
        Button_make_fun_button.clicked.connect(self.add_input)
        Button_make_fun_button.setFixedWidth(80)
        layout_boss.addWidget(Button_make_fun_button, alignment=Qt.AlignRight)

        layout_boss.addWidget(
            ButtonGroup(
                "Переменные",
                full_names=variable_full_names,
                buttons_action=self.insert_variable,
            )
        )
        layout_boss.addWidget(
            ButtonGroup(
                "Функции",
                full_names=function_full_names,
                buttons_action=self.insert_function,
            )
        )

        layout_boss.addSpacing(10)

        buttons_layout = QHBoxLayout()

        buttons_layout.setDirection(QHBoxLayout.RightToLeft)

        submit_button = QPushButton("Построить")
        reset_button = QPushButton("Сброс")

        submit_button.clicked.connect(self.plot)
        reset_button.clicked.connect(self.reset)

        submit_button.setDefault(True)

        buttons_layout.addWidget(submit_button)
        buttons_layout.addWidget(reset_button)

        self.subplots_checkbox = QCheckBox("Рисовать графики на отдельных осях")
        buttons_layout.addWidget(self.subplots_checkbox)

        buttons_layout.addStretch(1)

        layout_boss.addLayout(buttons_layout)

        self.setLayout(layout_boss)

    def add_input(self):
        self.num_of_input += 1

        graph_requester = GraphRequester(self.num_of_input)

        for line_edit in (graph_requester.LineEditX, graph_requester.LineEditY):
            line_edit.focused_in.connect(
                lambda line_edit=line_edit: self.set_focused_line_edit(line_edit)
            )

        graph_requester.LineEditGraf.focused_in.connect(
            lambda: self.set_focused_line_edit(None)
        )

        self.inputs_layout.insertWidget(self.inputs_layout.count() - 1, graph_requester)

        graph_requester.LineEditGraf.setFocus()

    def set_focused_line_edit(self, line_edit: QLineEdit | None):
        self.focused_line_edit = line_edit

    def scroll_bottom(self):
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    def insert_string(self, string: str, string_cursor_padding=-1):
        line_edit = self.focused_line_edit

        if line_edit is None:
            dlg = QMessageBox(
                QMessageBox.Warning,
                "Ошибка",
                "Выберите поле ввода выражения",
            )
            dlg.exec()

            return

        cusor_pos = line_edit.cursorPosition()
        text = line_edit.text()

        if string_cursor_padding < 1:
            string_cursor_padding = len(string)

        line_edit.setText(text[:cusor_pos] + string + text[cusor_pos:])
        line_edit.setCursorPosition(cusor_pos + string_cursor_padding)

        self.scroll.ensureWidgetVisible(line_edit)
        line_edit.setFocus()

    def insert_variable(self, name: str):
        self.insert_string(f" {name} ")

    def insert_function(self, name: str):
        string = f" {name}()"
        self.insert_string(string, len(string) - 1)  # len - 1 for cursor between braces

    def plot(self):
        xs, ys, labels = [], [], []

        for i in range(self.inputs_layout.count()):
            graph_requester = self.inputs_layout.itemAt(i).widget()

            if graph_requester is not None:
                x_expr = graph_requester.LineEditX.text()
                y_expr = graph_requester.LineEditY.text()
                label = graph_requester.LineEditGraf.text()

                if len(x_expr) * len(y_expr) == 0:
                    dlg = QMessageBox(
                        QMessageBox.Warning,
                        "Ошибка",
                        f'График "{label}" не задан',
                    )
                    dlg.exec()
                    return

                x = Parser(x_expr).evaluate(self.variable_values)
                y = Parser(y_expr).evaluate(self.variable_values)

                if size(x) != size(y):
                    dlg = QMessageBox(
                        QMessageBox.Critical,
                        "Ошибка",
                        "\n\n".join(
                            (
                                "Выражения имеют разную размерность",
                                f'y: "{y}" -> {size(y)}',
                                f'x: "{x}" -> {size(x)}',
                            )
                        ),
                    )
                    dlg.exec()

                    graph_requester.LineEditY.setFocus()
                    return

                xs.append(x)
                ys.append(y)
                labels.append(label)

        mult_subplots = self.subplots_checkbox.isChecked()

        self.graph = GraphWidget(xs, ys, labels, mult_plots=mult_subplots)

        self.graph.setWindowTitle("Графики")
        
        self.graph.exec()

    def reset(self):
        dlg = QMessageBox(
            QMessageBox.Question,
            "Очистка",
            "Вы уверены, что хотите очистить все введённые выражения?",
            buttons=QMessageBox.Yes | QMessageBox.No,
        )

        res = dlg.exec()

        if res != QMessageBox.Yes:
            return

        while self.inputs_layout.count() > 0:
            widget = self.inputs_layout.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)

        self.focused_line_edit = None

        self.num_of_input = 0

        self.add_input()

    def focus_first_input(self):
        first_graph_request = self.inputs_layout.itemAt(0).widget()
        if first_graph_request is not None:
            first_graph_request.LineEditGraf.setFocus()
