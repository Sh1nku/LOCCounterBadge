import copy
import json

import pybadges
from flask import Blueprint, make_response, Response


def construct_responses(repositories):
    response_functions = Blueprint('response_functions', __name__)

    @response_functions.route('/<repository_name>/responses/shields_v1', methods=['GET'])
    def shields_v1(repository_name):
        repository = repositories.get(repository_name)
        if not repository:
            return make_response('Could not find repository: {}'.format(repository_name), 404)
        response_type = repository.responses.get('response_shields_v1')
        if not response_type:
            return make_response('Response type not allowed for repository', 401)
        data = copy.deepcopy(response_type)
        data['message'] = '{:,}'.format(repository.get_loc())
        return make_response(data, 200, {'Cache-Control': 'no-cache'})

    @response_functions.route('/<repository_name>/responses/pybadges', methods=['GET'])
    def local(repository_name):
        repository = repositories.get(repository_name)
        if not repository:
            return make_response('Could not find repository: {}'.format(repository_name), 404)
        response_type = repository.responses.get('response_pybadges')
        if not response_type:
            return make_response('Response type not allowed for repository', 401)
        data = response_type
        ret = pybadges.badge(right_text='{:,}'.format(repository.get_loc()), **data)
        return Response(response=ret, status=200, mimetype='image/svg+xml', headers={'Cache-Control': 'no-cache'})

    return response_functions

