import json

from flask import Blueprint, make_response

import helpers


def construct_responses(config, memory):
    response_functions = Blueprint('response_functions', __name__)

    @response_functions.route('/<repository>/responses/shields_v1', methods=['GET'])
    def shields_v1(repository):
        if response := helpers.verify_config_response(repository, config, 'response_shields_v1'):
            return response
        x = config.get(repository, 'response_shields_v1')
        data = json.loads(config.get(repository, 'response_shields_v1'))
        if not memory.get(repository):
            make_response('Could not get repository LOC', 500)
        data['message'] = str(memory[repository])
        return make_response(data, 200)
    return response_functions

