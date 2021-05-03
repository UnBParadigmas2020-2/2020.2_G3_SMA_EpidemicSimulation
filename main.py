import time
from src.agent import MyAgent
from src.infectionmodel import InfectionModel
from src.plot import plot_cells_bokeh, plot_states_bokeh, get_column_data
from bokeh.io import show


if __name__ == "__main__":
    days = 100
    population = 400
    model = InfectionModel(population, 20, 20, ptrans=0.25, death_rate=0.01)

    for i in range(days):
        model.step()
        p1 = plot_states_bokeh(model, title='step=%s' % i) # Chart data visualization
        p2 = plot_cells_bokeh(model) # Grid agent visualization
        show(p1)
        time.sleep(2)
