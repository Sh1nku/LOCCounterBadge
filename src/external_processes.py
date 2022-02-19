import json
import os
import subprocess
import tempfile

from src.entities.LocCache import LocCache

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

def fetch_new_data(name, branch):
    proc = subprocess.run(['git', '-C', os.path.join(repos_dir, name), 'fetch'])
    if proc.returncode != 0:
        return False
    proc = subprocess.run(['git', '-C', os.path.join(repos_dir, name), 'checkout', 'origin/'+branch])
    return proc.returncode == 0


def count_lines_of_code(name, options=None):
    commit_hash = get_commit_hash(name)
    command = ['cloc', '--git', commit_hash, '--sum-one', '--json']
    with tempfile.NamedTemporaryFile('w') as tmp:
        if options:
            tmp.write(options)
            tmp.flush()
            command.extend(['--config', tmp.name])
        proc = subprocess.run(command, capture_output=True, cwd=os.path.join(repos_dir, name))
        if proc.returncode == 0:
            return LocCache(commit_hash, get_commit_date(name), json.loads(proc.stdout)['SUM']['code'])
    raise Exception('Could not count LOC for repo: {}'.format(name))


def get_commit_hash(name):
    command = ['git', 'rev-parse', 'HEAD']
    proc = subprocess.run(command, capture_output=True, cwd=os.path.join(repos_dir, name))
    if proc.returncode == 0:
        return proc.stdout.strip().decode('utf-8')
    return None

def get_commit_date(name):
    command = ['git', 'show', '-s', '--format=%ci', 'HEAD']
    proc = subprocess.run(command, capture_output=True, cwd=os.path.join(repos_dir, name))
    if proc.returncode == 0:
        return proc.stdout.strip().decode('utf-8')
    return None
