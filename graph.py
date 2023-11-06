from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class Graph:
    def __init__(
        self, x, y, labels, mult_subplots=0, xl="x", yl="y", linetype="k", lims=False
    ):
        # словарь из настроек?
        self.labels = labels
        self.__x = x
        self.__y = y
        self.__fig = Figure(figsize=(5, 4), dpi=100)
        self.__chb = mult_subplots
        self.__xl = xl
        self.__yl = yl

        self.draw_n_func_plot()

        self.draw_subplots()

        self.figure.tight_layout()

    def add_ax_labels(
        self,
        ax: plt.Axes,
    ):
        ax.set_xlabel(self.__xl)
        ax.set_ylabel(self.__yl)

    def draw_n_func_plot(self):  # много графиков на одном холсте
        if self.__chb == 0 and len(self.__x) > 0:
            self.__ax = self.__fig.add_subplot()

            for i in range(len(self.__x)):
                self.__ax.plot(self.__x[i], self.__y[i], label=self.labels[i])

            self.__ax.legend()
            self.add_ax_labels(self.__ax)

    def draw_subplots(
        self,
    ):
        if self.__chb == 1 and len(self.__x) > 0:
            for i in range(len(self.__x)):
                n = int(f"{len(self.__x)}1{i+1}")  # Nx1 grid (column), i+1 subplot

                axes = self.__fig.add_subplot(n)
                axes.set_title(f"График №{i+1}")
                axes.plot(self.__x[i], self.__y[i], label=self.labels[i])
                self.add_ax_labels(axes)

    @property
    def figure(
        self,
    ):
        return self.__fig
