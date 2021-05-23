import json
import os

from flask import make_response

cache_file = 'loc_cache.json'


def verify_config_data(repository, config):
    if repository not in config:
        return make_response('Repository "{}" not found'.format(repository), 404)
    if 'branch' not in config[repository]:
        return make_response('Branch not given in config', 500)
    if 'link' not in config[repository]:
        return make_response('Link not given in config', 500)

def verify_config_action(repository, config, action_name):
    if action_name not in config[repository]:
        valid_actions = [x.split('action_')[1] for x in config[repository] if x.startswith('action_')]
        return make_response('This action is not supported for the repository, valid actions are [{}]'.format(', '.join(valid_actions)), 400)

def verify_config_response(repository, config, response_name):
    if repository not in config:
        return make_response('Repository "{}" not found'.format(repository), 404)
    if response_name not in config[repository]:
        valid_responses = [x.split('response_')[1] for x in config[repository] if x.startswith('response_')]
        return make_response('This response is not supported for the repository, valid responses are [{}]'.format(', '.join(valid_responses)), 400)

def update_lines_of_code(memory, repository, lines):
    memory[repository] = lines
    with open(cache_file, 'w') as f:
        f.write(json.dumps(memory))


def read_lines_of_code():
    if not os.path.exists(cache_file):
        return {}
    with open(cache_file, 'r') as f:
        return json.loads(f.read())
