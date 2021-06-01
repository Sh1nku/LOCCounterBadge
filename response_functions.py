import json

import pybadges
from flask import Blueprint, make_response, Response

import helpers


def construct_responses(config, memory):
    response_functions = Blueprint('response_functions', __name__)

    @response_functions.route('/<repository>/responses/shields_v1', methods=['GET'])
    def shields_v1(repository):
        if response := helpers.verify_config_response(repository, config, 'response_shields_v1'):
            return response
        data = json.loads(config.get(repository, 'response_shields_v1'))
        if not memory.get(repository):
            make_response('Could not get repository LOC', 500)
        data['message'] = '{:,}'.format(memory[repository])
        return make_response(data, 200)


    @response_functions.route('/<repository>/responses/pybadges', methods=['GET'])
    def local(repository):
        function = 'response_pybadges'
        if response := helpers.verify_config_response(repository, config, function):
            return response
        data = json.loads(config.get(repository, function))
        if not memory.get(repository):
            make_response('Could not get repository LOC', 500)
        ret = pybadges.badge(right_text='{:,}'.format(memory[repository]), **data)
        return Response(response=ret, status=200, mimetype='image/svg+xml')

    return response_functions

