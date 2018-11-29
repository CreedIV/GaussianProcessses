from gaussianProcessUtils import resample_chain

import numpy as np
import random
from bokeh.layouts import  layout, widgetbox, gridplot
from bokeh.models import Slider, Button,SingleIntervalTicker, LinearAxis
from bokeh.io import curdoc
from bokeh.plotting import figure, ColumnDataSource

def new_givens():
    numpoints=samples_slider.value
    xs = [n+1 for n in range(numpoints)]
    given = int(given_slider.value*numpoints)
    Xgiven = random.sample(xs, given)
    Ygiven = [random.gauss(0,1) for _ in Xgiven]
    givens.data = dict(xs=Xgiven, ys=Ygiven)
    resample_wrapper()

def resample_wrapper():
    numpoints=samples_slider.value
    source.data = resample_chain(numpoints, theta1_slider.value, givens.data)
    xs = source.data['xs']
    ys = source.data['ys']
    std = source.data['std']
    wX = np.append(xs, xs[::-1])
    wY = np.append(ys+std, (ys-std)[::-1])
    source2.data=dict(wX=wX,wY=wY)
    
def given_wrapper(old, new):
    if (int(old*samples_slider.value) != int(new*samples_slider.value)):
        new_givens()

source = ColumnDataSource(data=dict(xs=[0], ys=[0], std=[0], color=['b']))
source2 = ColumnDataSource(data=dict(wX=[0], wY=[0]))
givens = ColumnDataSource(data=dict(xs=[0], ys=[0]))

plot = figure(y_range=(-5, 5), x_range=(-1, 20), plot_width=800, plot_height=400, x_axis_type=None, y_axis_label='y_i value')
plot.patch('wX','wY', source=source2, color='cyan') 
plot.line(x='xs', y='ys', source=source)
plot.scatter('xs', 'ys',color='color', source=source, line_width=3, line_alpha=0.6)
ticker = SingleIntervalTicker(interval=1, num_minor_ticks=0)
xaxis = LinearAxis(ticker=ticker, axis_label = 'y index')
plot.add_layout(xaxis, 'below')

samples_slider = Slider(start=3, end=20, value=10, step=1,title="Number of points")
given_slider = Slider(start=0, end=1, value=.1, step=.1,title="% of given points")
theta1_slider = Slider(start=0.01, end=1, value=.12, step=.01,title="Theta_1")
resample_Button = Button(label="Resample unknowns")

samples_slider.on_change('value', lambda attr, old, new: new_givens())
given_slider.on_change('value', lambda attr, old, new: given_wrapper(old, new))
theta1_slider.on_change('value', lambda attr, old, new: resample_wrapper())
resample_Button.on_click( lambda :resample_wrapper())

controls = [samples_slider,given_slider, theta1_slider,resample_Button]
inputs = widgetbox(*controls, sizing_mode='fixed')
l = gridplot([[inputs],[plot]])

resample_wrapper()
curdoc().add_root(l)