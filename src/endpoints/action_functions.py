import hashlib
import hmac
import json
import sys

from flask import Blueprint, make_response, request

from src.external_processes import fetch_new_data, count_lines_of_code


def construct_actions(repositories):
    action_functions = Blueprint('action_functions', __name__)

    @action_functions.route('/<repository_name>/actions/github', methods=['POST'])
    def github(repository_name):
        repository = repositories.get(repository_name)
        if not repository:
            return make_response('Could not find repository', 404)
        if not 'action_github' in repository.actions:
            return make_response('This action is not allowed for this repository', 401)
        # Verify not forged request
        if not request.headers.get('X-GitHub-Event') or not request.headers.get('X-Hub-Signature') or not request.is_json:
            return make_response('Not valid request', 400)
        secret = repository.actions['action_github'].get('secret')
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
        if not data.get('ref') or not data['ref'] == 'refs/heads/'+repository.branch:
            return make_response('Not the correct branch', 202)
        if not (commit := data.get('after')):
            return make_response('Commit not given', 400)
        if not fetch_new_data(repository.name, repository.branch):
            return make_response('could not fetch new data', 500)
        try:
            repository.cache = count_lines_of_code(repository.name, repository.cloc_options)
            # Updates either the local cache or the cache file
            repository.get_loc()
        except Exception as e:
            print('Failed in reading lines of code: {}'.format(repository.name), sys.stderr)
            make_response('Could not count lines of code', 500)
        return make_response('', 200)

    return action_functions
