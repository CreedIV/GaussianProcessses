def GP3(doc):
    from gaussianProcessUtils import drawContour, resample

    from bokeh.layouts import  widgetbox, gridplot
    from bokeh.models import Slider, Button, SingleIntervalTicker, LinearAxis
    from bokeh.plotting import figure, ColumnDataSource

    def resample_wrapper():
        numpoints = 1
        source.data = resample(numpoints, covariance_slider.value)
        source3.data = dict(xs=[n+1 for n in range(numpoints+1)], ys=[source.data['x1'][0],source.data['x2'][0]])

    def update_all():
        source2.data = drawContour(covariance_slider.value)
        resample_wrapper()
 
    source = ColumnDataSource(data=dict(x1=[0], x2=[0]))
    source2 = ColumnDataSource(data=dict(xs=[0], ys=[0]))
    source3 = ColumnDataSource(data=dict(xs=[0], ys=[0]))

    plot = figure(y_range=(-3, 3), x_range=(-3, 3), plot_width=400, plot_height=400, x_axis_label='y1', y_axis_label='y2')
    plot.scatter('x1', 'x2', source=source, line_width=3, line_alpha=0.6)
    plot.multi_line(xs='xs', ys='ys', line_color='line_color', source=source2)

    plot2 = figure(y_range=(-3, 3), x_range=(0, 3), plot_width=400, plot_height=400, x_axis_type=None, y_axis_label='y_i value')
    plot2.line(x='xs', y='ys', source=source3)
    plot2.scatter('xs', 'ys', source=source3)
    ticker = SingleIntervalTicker(interval=1, num_minor_ticks=0)
    xaxis = LinearAxis(ticker=ticker, axis_label = 'y index')
    plot2.add_layout(xaxis, 'below')
    
    resample_Button = Button(label="Resample")
    covariance_slider = Slider(start=0.0, end=.99, value=0, step=.01,title="Covariance")

    resample_Button.on_click( lambda :resample_wrapper())
    covariance_slider.on_change('value', lambda attr, old, new: update_all())

    controls = [covariance_slider, resample_Button]
    inputs = widgetbox(*controls, sizing_mode='fixed')
    l = gridplot([[inputs],[plot, plot2]])

    update_all()
    doc.add_root(l)