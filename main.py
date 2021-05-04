import time
from src.agent import MyAgent
from src.infectionmodel import InfectionModel
from src.plot import plot_cells_bokeh, plot_states_bokeh
from bokeh.io import curdoc
from bokeh.layouts import row, column, layout
from bokeh.models import Slider, Button

# Widgets definitions
population = Slider(title="Population", value=400, start=1, end=1000, step=1)
death_rate = Slider(title="Death Probabiblity per Day Infected", value=0.01, start=0.01, end=1, step=0.01)
transmission_rate = Slider(title="Transmission Rate", value=0.25, start=0.01, end=1, step=0.01)
initial_infected = Slider(title="Initial Number of Infected", value=20, start=1, end=1000, step=1)
area = Slider(title="Area Size", value=20, start=10, end=30, step=1)
wait_for_input = Button(label="Start Simulation")

# Initial setup
i = 0
model = InfectionModel(400, 20, 20, ptrans=0.25, death_rate=0.01, initial_infected=10)
p1 = plot_states_bokeh(model, title='step=%s' % i)
p2 = plot_cells_bokeh(model)


# Wait for user to start simulation
def start_sim():
    global p1, p2, model, i
    if initial_infected.value >= population.value:
        initial_infected.value = population.value-1

    model = InfectionModel(population.value, area.value, area.value, ptrans=transmission_rate.value, death_rate=death_rate.value, initial_infected=initial_infected.value)
    p1 = plot_states_bokeh(model, title='step=')  # Chart data visualization
    p2 = plot_cells_bokeh(model)  # Grid agent visualization
    curdoc().add_periodic_callback(callback, 50)


# Update plots
def callback():
    global p1, p2, model, i
    model.step()
    p1 = plot_states_bokeh(model, title='step=%s' % i)
    p2 = plot_cells_bokeh(model)
    lay_out.children[0] = p1
    lay_out.children[1] = p2
    if i > 100:
        exit()
    i += 1


# Bokeh variables required to open server
wait_for_input.on_click(start_sim)
lay_out = row(p1, p2)
lay_out_input = column(population, death_rate, transmission_rate, initial_infected, area, wait_for_input)
curdoc().add_root(column(lay_out, lay_out_input))
