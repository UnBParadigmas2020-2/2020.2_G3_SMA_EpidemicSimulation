import time
from src.agent import MyAgent
from src.infectionmodel import InfectionModel
from src.plot import plot_cells_bokeh, plot_states_bokeh, get_column_data
from bokeh.io import show, curdoc
from bokeh.layouts import row, column, layout
from bokeh.io.state import State


days = 100
population = 400
model = InfectionModel(population, 20, 20, ptrans=0.25, death_rate=0.01)

model.step()
p1 = plot_states_bokeh(model, title='step=')  # Chart data visualization
p2 = plot_cells_bokeh(model)  # Grid agent visualization
i = 0


def callback():
    model.step()
    global p1, p2, i
    p1 = plot_states_bokeh(model, title='step=%s' % i)
    p2 = plot_cells_bokeh(model)
    lay_out.children[0] = p1
    lay_out.children[1] = p2
    if i >= 100:
        exit()
    i += 1


lay_out = row(p1, p2)
curdoc().add_root(lay_out)
curdoc().add_periodic_callback(callback, 50)
