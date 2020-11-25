import argparse
import random
import sys

import google.auth
from google.auth.transport.requests import AuthorizedSession
import polling
import os
from requests.exceptions import HTTPError

from jade_job import __version__ as jade_job_version


class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        """Print help message by default."""
        sys.stderr.write(f'error: {message}\n')
        self.print_help()
        sys.exit(2)


def alert(job_uuid, job_status):
    title = 'Jade Job Status'
    text =  f"Job {job_uuid} completed with status: {job_status}"
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def get_authorized_session():
    credentials, project = google.auth.default(scopes=['openid', 'email', 'profile'])
    return AuthorizedSession(credentials)


def run(arguments=None):
    parser = DefaultHelpParser(description='A simple Jade Job CLI.')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + jade_job_version)
    parser.add_argument('job_id', help="The Jade job id to poll")
    parser.add_argument('-e', '--env', help='The Jade environment to target, defaults to dev', choices=['dev', 'prod'], default='dev')
    parser.add_argument('-t', '--timeout', help="Timeout for polling", type=int, default=3600)
    args = parser.parse_args(arguments)

    if not sys.argv[1:]:
        parser.error('No commands or arguments provided!')

    if args.job_id:
        poll_job(args.job_id, args.timeout, args.env)


def poll_job(job_id: str, timeout: int, env: str):
    # TODO
    try:
        polling.poll(lambda: is_done(job_id, env), step=10, step_function=step_function, timeout=timeout)
        status = check_job_status(job_id, env)
        alert(job_id, status)
        # is done after poll
    except polling.TimeoutException as te:
        while not te.values.empty():
            # log errors TODO
            print(te.values.get(), file=sys.stderr)


def check_job_status(job_id: str, env: str):
    authed_session = get_authorized_session()
    base_url = {'dev': 'https://jade.datarepo-dev.broadinstitute.org',
                'prod': 'https://jade-terra.datarepo-prod.broadinstitute.org'}[env]
    response = authed_session.get(f'{base_url}/api/repository/v1/jobs/{job_id}')
    if response.ok:
        return response.json()['job_status']
    else:
        raise HTTPError(f'Bad response, got code of: {response.status_code}')


def is_done(job_id: str, env: str) -> bool:
    # if "running" then we want to keep polling, so false
    # if "succeeded" then we want to stop polling, so true
    # if "failed" then we want to stop polling, so true
    status = check_job_status(job_id, env)
    return status in ['succeeded', 'failed']


def step_function(step: int) -> int:
    return random.randint(step, step + 10)
