
#import pandas as pd
#import plotly.express as px
from dash import Dash  #,dcc,html
#from dash.dependencies import Input, Output
from model import Model, params #Sprite,
from view import View

#import datetime
#import plotly
#import numpy as np




class Controller:
    def __init__(self,model,app):
        self.app = app
        view = View(model,self.app)
        view.make_layout()
        view.update_view()

    def start(self):
        self.app.run_server(debug=True)


if __name__ == '__main__':
    model = Model(params)
    app = Dash(__name__)
    controller = Controller(model,app)
    controller.start()
