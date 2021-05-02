from agents.infectionmodel import InfectionModel
from agents.agent import MyAgent, plot_cells_bokeh, plot_states_bokeh, get_column_data
import time

if __name__ == "__main__":
    steps=100
    pop=400
    model = InfectionModel(pop, 20, 20, ptrans=0.25, death_rate=0.01)
    for i in range(steps):
        model.step()    
        plot_states_bokeh(model,title='step=%s' %i)
        p2=plot_cells_bokeh(model)
        print(get_column_data(model))
        time.sleep(0.02)
