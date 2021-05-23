import configparser
import os
import flask

from action_functions import construct_actions, read_lines_of_code
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


config = parse_config('conf.d', 'config.cfg')
app = flask.Flask(__name__)
memory = read_lines_of_code()

construct_exceptions(app)
app.register_blueprint(construct_responses(config, memory))
app.register_blueprint(construct_actions(config, memory))

app.config["DEBUG"] = config.getboolean('general', 'debug', fallback=False)
app.run(port=config.get('general', 'port', fallback=20300),
        host=config.get('general', 'host', fallback='0.0.0.0'))
