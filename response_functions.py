from flask import Blueprint

def construct_responses(config, memory):
    response_functions = Blueprint('response_functions', __name__)

    @response_functions.route('/responses/shields_v1', methods=['GET'])
    def shields_v1():
        pass
    return response_functions

