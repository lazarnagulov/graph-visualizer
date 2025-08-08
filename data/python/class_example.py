import math
import matplotlib.pyplot as plt

class DataGenerator:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def generate_data(self) -> list[float]:
        return [2 + math.sqrt(x) for x in range(self.start, self.end)]

class Plotter:
    def __init__(self, x: list[int], y: list[float]) -> None:
        self.x = x
        self.y = y

    def plot(self) -> None:
        plt.plot(self.x, self.y, marker='o')
        plt.title('Plot of y = 2 + sqrt(x)')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.show()

def main() -> None:
    start, end = 0, 20
    data_gen = DataGenerator(start, end)
    y_values = data_gen.generate_data()
    x_values = list(range(start, end))

    plotter = Plotter(x_values, y_values)
    plotter.plot()

if __name__ == "__main__":
    main()
