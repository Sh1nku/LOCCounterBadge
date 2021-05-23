import hashlib
import hmac
import json
import os

from flask import Blueprint, make_response, request

from external_processes import clone_repo_if_not_exists, count_lines_of_code, fetch_new_data


def construct_actions(config, memory):
    action_functions = Blueprint('action_functions', __name__)

    @action_functions.route('/<repository>/actions/github', methods=['POST'])
    def github(repository):
        if response := verify_config_data(repository, 'action_github', config):
            return response
        # Verify not forged request
        if not request.headers.get('X-GitHub-Event') or not request.headers.get('X-Hub-Signature') or not request.is_json:
            return make_response('Not valid request', 400)
        config_data = json.loads(config.get(repository, 'action_github'))
        secret = config_data.get('secret')
        if not secret:
            return make_response('Secret not given in config', 500)
        request_hash = request.headers['X-Hub-Signature']
        content_hash = 'sha1='+hmac.new(secret.encode('utf-8'), request.get_data(), hashlib.sha1).hexdigest()
        if not hmac.compare_digest(request_hash, content_hash):
            return make_response('Hashes do not match', 400)

        # Verify relevant request
        if not request.headers['X-GitHub-Event'] == 'push':
            return make_response('Not push event', 202)
        data = request.get_json()
        if not data.get('ref') or not data['ref'] == 'refs/heads/'+config.get(repository, 'branch'):
            return make_response('Not the correct branch', 202)

        # Request checks out and is on a branch we want to update
        if not clone_repo_if_not_exists(config.get(repository, 'link'), repository):
            return make_response('Error in cloning repo', 500)
        if not (commit := data.get('after')):
            return make_response('Commit not given', 400)

        if not fetch_new_data(repository):
            return make_response('could not fetch new data', 500)
        status, lines = count_lines_of_code(repository, commit)
        if not status:
            return make_response('Error counting lines of code', 500)
        update_lines_of_code(memory, repository, lines)
        return make_response('', 200)



    return action_functions

def verify_config_data(repository, action_name, config):
    if repository not in config:
        return make_response('Repository "{}" not found'.format(repository), 400)
    if action_name not in config[repository]:
        valid_actions = [x.split('action_')[1] for x in config[repository] if x.startswith('action_')]
        return make_response('This action is not supported for the repository, valid actions are [{}]'.format(', '.join(valid_actions)), 500)
    if 'branch' not in config[repository]:
        return make_response('Branch not given in config', 500)
    if 'link' not in config[repository]:
        return make_response('Link not given in config', 500)


cache_file = 'loc_cache.json'


def update_lines_of_code(memory, repository, lines):
    memory[repository] = lines
    with open(cache_file, 'w') as f:
        f.write(json.dumps(memory))

def read_lines_of_code():
    if not os.path.exists(cache_file):
        return {}
    with open(cache_file, 'r') as f:
        return json.loads(f.read())

