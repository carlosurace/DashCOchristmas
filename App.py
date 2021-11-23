'''
Created on Jun 24, 2020

@author: Carlo
'''
import dash
from flask_caching import Cache
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
assets_path = THIS_FOLDER +'/assets'
app = dash.Dash( __name__,assets_folder=assets_path,suppress_callback_exceptions=True)
server = app.server
server.config.update(
    SECRET_KEY=os.urandom(12),
)
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': THIS_FOLDER+'/Cache',
    'CACHE_DEFAULT_TIMEOUT': 922337203685477580,
    'CACHE_OPTIONS':{}
})
app.config.suppress_callback_exceptions = True