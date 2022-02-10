#!/usr/bin/python3

import configparser
import os
import sys

import flask

import external_processes
from action_functions import construct_actions
from exceptions import construct_exceptions
from response_functions import construct_responses
from src.Repository import Repository


def parse_config(path, file):
    cfg = configparser.ConfigParser()
    if not cfg.read(os.path.join(path, file), encoding='utf-8'):
        print("{} is empty or not found. Create a valid cfg file from the template".format(file))
        exit()
    else:
        cfg.read(os.path.join(path, file), encoding='utf-8')
        return cfg




config = parse_config('conf.d', 'config.cfg')
app = flask.Flask(__name__)
repositories = {}
for section in [x for x in config.sections() if x != 'general']:
    repositories[section] = Repository(config, section)

try:
    os.mkdir('cache')
except FileExistsError:
    pass

construct_exceptions(app)
app.register_blueprint(construct_responses(repositories))
app.register_blueprint(construct_actions(repositories))

app.config["DEBUG"] = config.getboolean('general', 'debug', fallback=False)
app.run(port=config.get('general', 'port', fallback=20300),
        host=config.get('general', 'host', fallback='0.0.0.0'))
