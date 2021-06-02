#!/usr/bin/python3

import configparser
import os
import flask

import external_processes
import helpers
from action_functions import construct_actions
from exceptions import construct_exceptions
from response_functions import construct_responses


def parse_config(path, file):
    cfg = configparser.ConfigParser()
    if not cfg.read(os.path.join(path, file), encoding='utf-8'):
        print("{} is empty or not found. Create a valid cfg file from the template".format(file))
        exit()
    else:
        cfg.read(os.path.join(path, file), encoding='utf-8')
        return cfg

def init_repos(config, memory):
    for section in [x for x in config.sections() if x != 'general']:
        if response := helpers.verify_config_data(section, config):
            print(response.get_data())
            continue
        if not external_processes.clone_repo_if_not_exists(config.get(section, 'link'), section):
            print('Could not clone repo: {}'.format(section))
            continue
        if not external_processes.fetch_new_data(section, config.get(section, 'branch')):
            print('Could download newest data: {}'.format(section))
            continue
        status, loc = external_processes.count_lines_of_code(section, config.get(section, 'branch'), config.get(section, 'cloc_options', fallback=None))
        if not status:
            print('Error in counting lines of code: {}'.format(section))
            continue
        helpers.update_lines_of_code(memory, section, loc)


config = parse_config('conf.d', 'config.cfg')
app = flask.Flask(__name__)
memory = helpers.read_lines_of_code()
init_repos(config, memory)

construct_exceptions(app)
app.register_blueprint(construct_responses(config, memory))
app.register_blueprint(construct_actions(config, memory))

app.config["DEBUG"] = config.getboolean('general', 'debug', fallback=False)
app.run(port=config.get('general', 'port', fallback=20300),
        host=config.get('general', 'host', fallback='0.0.0.0'))
