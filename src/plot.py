import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool, Legend, LinearColorMapper
from bokeh.plotting import figure
from bokeh.models.glyphs import Line
from bokeh.palettes import Category10


# Pivot the model dataframe to get states count at each step
def get_column_data(model):
    agent_state = model.datacollector.get_agent_vars_dataframe()
    data_table = pd.pivot_table(agent_state.reset_index(), index='Step',
                                columns='State', aggfunc=np.size, fill_value=0)
    labels = ['Susceptible', 'Infected', 'Recovered', 'Deceased']
    data_table.columns = labels[:len(data_table.columns)]
    return data_table


# Get grid cell states
def grid_values(model):
    agent_counts = np.zeros((model.grid.width, model.grid.height))
    df = pd.DataFrame(agent_counts)
    for cell in model.grid.coord_iter():
        agents, x, y = cell
        c = None
        for a in agents:
            c = a.state
        df.iloc[x, y] = c
    return df


# Plot cases per state
def plot_states_bokeh(model, title=''):
    data_table = get_column_data(model)
    data_table = data_table.reset_index()
    source = ColumnDataSource(data_table)
    i = 0
    colors = Category10[4]
    items = []
    plot = figure(plot_width=600, plot_height=400,
                  tools=[], title=title, x_range=(0, 100))
    for c in data_table.columns[1:]:
        line = Line(x='Step', y=c,
                    line_color=colors[i], line_width=3, line_alpha=.8, name=c)
        glyph = plot.add_glyph(source, line)
        i += 1
        items.append((c, [glyph]))

    plot.xaxis.axis_label = 'Step'
    plot.add_layout(Legend(location='center_right',
                           items=items))
    plot.background_fill_color = "#e1e1ea"
    plot.background_fill_alpha = 0.5
    plot.legend.label_text_font_size = "10pt"
    plot.title.text_font_size = "15pt"
    plot.toolbar.logo = None
    plot.sizing_mode = 'scale_height'
    return plot


def plot_cells_bokeh(model):
    w = model.grid.width
    df = grid_values(model)
    df = pd.DataFrame(df.stack(), columns=['value']).reset_index()
    columns = ['value']
    x = [(i, "@%s" % i) for i in columns]
    hover = HoverTool(
        tooltips=x, point_policy='follow_mouse')
    colors = Category10[3]
    mapper = LinearColorMapper(
        palette=colors, low=df.value.min(), high=df.value.max())
    plot = figure(plot_width=500, plot_height=500, tools=[
               hover], x_range=(-1, w), y_range=(-1, w))
    plot.rect(x="level_0", y="level_1", width=1, height=1,
           source=df,
           fill_color={'field': 'value', 'transform': mapper},
           line_color='black')
    plot.background_fill_color = "black"
    plot.grid.grid_line_color = None
    plot.axis.axis_line_color = None
    plot.toolbar.logo = None
    return plot
