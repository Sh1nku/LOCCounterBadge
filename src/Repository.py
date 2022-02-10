import configparser
import json
import os
import sys

from src import external_processes


class Repository:
    def __init__(self, config: configparser.ConfigParser, section: str):
        self.name = section
        self.commit_hash = None
        self.loc = None
        self.branch = config.get(section, 'branch', fallback=None)
        self.link = config.get(section, 'link', fallback=None)
        self.cloc_options = config.get(section, 'cloc_options', fallback=None)
        self.cache_file_location = 'cache/' + section + '.json'
        self.actions = {}
        self.responses = {}
        for x in config[section]:
            if x.startswith('action_'):
                self.actions[x] = json.loads(config[section][x])
        for x in config[section]:
            if x.startswith('response_'):
                self.responses[x] = json.loads(config[section][x])
        try:
            if not self.branch:
                raise Exception('Branch not given in config')
            if not self.link:
                raise Exception('Link not given in config')
            if not external_processes.clone_repo_if_not_exists(self.link, self.name):
                raise Exception('Could not clone repo: {}'.format(section))
            if not external_processes.fetch_new_data(self.name, self.branch):
                raise Exception('Could download newest data: {}'.format(section))
            self.commit_hash, self.loc = \
                external_processes.count_lines_of_code(section,
                                                       self.cloc_options)
        except Exception as e:
            print(e, file=sys.stderr)
            exit(1)

    def get_loc(self):
        if os.path.exists(self.cache_file_location):
            with open(self.cache_file_location, 'r') as f:
                tmp = json.loads(f.read())
                if tmp['commit_hash'] == self.commit_hash:
                    return self.loc
                return tmp.loc
        else:
            with open(self.cache_file_location, 'w') as f:
                f.write(json.dumps({
                    'loc': self.loc,
                    'commit_hash': self.commit_hash
                }))
                return self.loc
