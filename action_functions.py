import hashlib
import hmac
import json
import os

from flask import Blueprint, make_response, request

import helpers
from external_processes import clone_repo_if_not_exists, count_lines_of_code, fetch_new_data


def construct_actions(config, memory):
    action_functions = Blueprint('action_functions', __name__)

    @action_functions.route('/<repository>/actions/github', methods=['POST'])
    def github(repository):
        if response := helpers.verify_config_data(repository, config):
            return response
        if response := helpers.verify_config_action(repository, config, 'action_github'):
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

        if not fetch_new_data(repository, config.get(repository, 'branch')):
            return make_response('could not fetch new data', 500)
        status, lines = count_lines_of_code(repository, config.get(repository, 'branch'))
        if not status:
            return make_response('Error counting lines of code', 500)
        helpers.update_lines_of_code(memory, repository, lines)
        return make_response('', 200)



    return action_functions
