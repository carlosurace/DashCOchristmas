'''
Created on Jun 24, 2020

@author: Carlo
'''
import dash

app = dash.Dash( suppress_callback_exceptions=True)
server = app.server
app.config.suppress_callback_exceptions = True