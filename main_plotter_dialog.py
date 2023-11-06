import sys
import os
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QApplication

import numpy as np

from dialog import PlotterDialog


def main():
    app = QApplication(sys.argv)

    variables = [chr(ord("a") + i) for i in range(4)]

    dlg = PlotterDialog(
        variable_values={key: np.sort(np.random.random(10)) * 10 for key in variables},
        variable_full_names={key: key.upper() for key in variables},
    )
    dlg.show()

    sys.exit(app.exec())

main()
