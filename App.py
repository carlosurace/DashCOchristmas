'''
Created on Jun 24, 2020

@author: Carlo
'''
import dash
from flask_caching import Cache

app = dash.Dash( suppress_callback_exceptions=True)
server = app.server
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'Bids',
    'CACHE_DEFAULT_TIMEOUT': 3600,
})
app.config.suppress_callback_exceptions = True