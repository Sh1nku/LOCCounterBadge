from flask import Blueprint, make_response


def construct_actions(config):
    action_functions = Blueprint('action_functions', __name__)

    @action_functions.route('/<repository>/actions/github', methods=['POST'])
    def github(repository):
        if response := verify_config_uses_action(repository, 'action_github', config):
            return response

        return make_response("", 200)

    return action_functions

def verify_config_uses_action(repository, action_name, config):
    if repository not in config:
        return make_response('Repository "{}" not found'.format(repository), 400)
    if action_name not in config[repository]:
        valid_actions = [x.split('action_')[1] for x in config[repository] if x.startswith('action_')]
        return make_response('This action is not supported for the repository, valid actions are [{}]'.format(', '.join(valid_actions)), 500)

