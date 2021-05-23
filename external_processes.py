import json
import os
import subprocess

repos_dir = 'repos'

def clone_repo_if_not_exists(link, name):
    try:
        os.mkdir(repos_dir)
    except FileExistsError:
        pass

    if os.path.exists(os.path.join(repos_dir, name)) and os.path.isdir(os.path.join(repos_dir, name)):
        return True
    proc = subprocess.run(['git', 'clone', link, os.path.join(repos_dir, name)])
    return proc.returncode == 0

def fetch_new_data(name):
    proc = subprocess.run(['git', '-C', os.path.join(repos_dir, name), 'fetch'])
    return proc.returncode == 0

def count_lines_of_code(name, commit):
    proc = subprocess.run(['cloc', '--git', commit, '--sum-one', '--json', os.path.join(repos_dir, name)], capture_output=True)
    if proc.returncode == 0:
        return True, json.loads(proc.stdout)['SUM']['code']
    return False, 0
