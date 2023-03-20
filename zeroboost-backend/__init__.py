from flask import Flask, request, jsonify
from .src.replay_aggregator import ReplayAggregator
from flask_cors import cross_origin
from .db import init_db, db_session
from .db.models import Player


import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    init_db()
    

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
   


    @app.get('/<platform>/<player_id>/')
    @cross_origin()
    def get_dashboard(platform,player_id):
        app.logger.info('Request seen')
        replay_agg = ReplayAggregator(platform = platform, player_id = player_id)
        return jsonify(replay_agg.get_replays())
    
    @app.get('/players')
    def get_all_players():
        app.logger.info('Getting players')
        return jsonify(Player.query.all())



    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app


