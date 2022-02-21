#import pandas as pd
import plotly.express as px
from dash import dcc,html #,Dash
from dash.dependencies import Input, Output
#from model2 import Model, Sprite, params
#import numpy as np

class View:

    def __init__(self,model,app):
        self.model = model
        self.app = app

    def make_layout(self):
        intro_text = dcc.Markdown('## Pandemic simulator ')
        graph_component = html.Div(
            [dcc.Graph(id='graph'),
            dcc.Interval(id='interval-component',
            interval=10000//self.model.params['fps'],
            # in milliseconds
            n_intervals=0)])
        model_text = html.Div(html.P(f"""{self.model.params}"""))
        slide_text = dcc.Markdown('#### Parameters')

        self.distance = Slide(self.app,
            self.model,0,40,5,"distance")
        self.chance_of_death = Slide(self.app,
            self.model,0,100,5,"chance_of_death")

        self.app.layout = html.Div([intro_text,
                               model_text,
                               graph_component,
                               slide_text,
                               self.distance.component,
                               self.chance_of_death.component,
                              ])

    def update_view(self):
        """Set up the callbacks.
        #   There are three, one for the graph
        and one each for the sliders"""
        @self.app.callback(Output("graph","figure"),
                     Input("interval-component","n_intervals"))
        def update(n_intervals):
            df = self.model.update_all()

            return px.scatter(df,x="x",y="y",
                              color = "well",
                              color_discrete_map= {True: 'blue',
                                                  False: 'red'},
                              range_x=[0,self.model.params['width']],
                              range_y=[0,self.model.params['height']])

        self.distance.callback()
        self.chance_of_death.callback()


class Slide:

    def __init__(self,app,model,mn,mx,interval,name):

        self.app = app
        self.model = model
        self.mn = mn
        self.mx = mx
        self.interval = interval

        self.name = name
        self.component = self.make_component()


    def make_component(self):
        value = self.model.params[self.name]
        comp = html.Div([
                    dcc.Slider(self.mn,
                               self.mx,
                               self.interval,
                               value=value,
                               id=f'{self.name}-slider',
                               tooltip={"placement": "right",
                                       "always_visible": True}),
                    html.Div(id=f'{self.name}-container-slider')])
        return comp

    def callback(self):

        @self.app.callback(Output(f'{self.name}-container-slider',
                           'children'),
                      Input(f'{self.name}-slider','value') )
        def update_self(value):
            self.model.params[self.name]=value
            return f'{self.name} is {self.model.params[self.name]}'

        return update_self
