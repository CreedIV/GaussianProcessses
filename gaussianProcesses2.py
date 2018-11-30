from gaussianProcessUtils import drawContour, resample_givenX1, update_normal

from bokeh.layouts import  widgetbox, gridplot
from bokeh.models import Slider
from bokeh.io import curdoc
from bokeh.plotting import figure, ColumnDataSource

def resample_wrapper():
    source.data=resample_givenX1(samples_slider.value,covariance_slider.value, x1_slider.value)

def update_xs():
    resample_wrapper()
    source3.data = update_normal(covariance_slider.value, x1_slider.value)
    
    
def update_all():
    source2.data = drawContour(covariance_slider.value)
    resample_wrapper()
    source3.data = update_normal(covariance_slider.value, x1_slider.value)

source = ColumnDataSource(data=dict(x1=[0], x2=[0]))
source2 = ColumnDataSource(data=dict(xs=[0], ys=[0]))
source3 = ColumnDataSource(data=dict(xs=[0], ys=[0]))

plot = figure(y_range=(-3, 3), x_range=(-3, 3), plot_width=400, plot_height=400, x_axis_label='y1', y_axis_label='y2')
plot.scatter('x1', 'x2', source=source, line_width=3, line_alpha=0.6)
plot.multi_line(xs='xs', ys='ys', line_color='line_color', source=source2)
plot.line(x='xs', y='ys', source=source3, line_width=3, line_alpha=0.6, line_color='red')

covariance_slider = Slider(start=0.0, end=.99, value=0, step=.01,title="Covariance")
samples_slider = Slider(start=1, end=100, value=10, step=1,title="Number of Samples")
x1_slider = Slider(start=-2.5, end=2.5, value=0, step=.1,title="y1")

covariance_slider.on_change('value', lambda attr, old, new: update_all())
samples_slider.on_change('value', lambda attr, old, new: resample_wrapper())
x1_slider.on_change('value', lambda attr, old, new: update_xs())

controls = [covariance_slider, samples_slider, x1_slider]
inputs = widgetbox(*controls, sizing_mode='fixed')
l = gridplot([[inputs],[plot]])

update_all()
curdoc().add_root(l)