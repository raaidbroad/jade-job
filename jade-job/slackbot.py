import os
import requests
import urllib3

from vault import Vault

urllib3.disable_warnings()


# Slack-specific parameters
SLACK_BASE_API = 'https://slack.com/api'

# Slack API Methods
USER_LOOKUP_METHOD = 'users.lookupByEmail'
OPEN_CONVERSATION = 'conversations.open'
POST_MESSAGE_METHOD = 'chat.postMessage'
FILE_UPLOAD_METHOD = 'files.upload'
DELETE_MESSAGE_METHOD = 'chat.delete'

# Bot-specific parameters
VAULT_SLACK_CREDENTIALS_PATH = os.environ['VAULT_SLACK_CREDENTIALS_PATH']


class SlackBot:

    def __init__(self, vault_credentials_path=VAULT_SLACK_CREDENTIALS_PATH, slack_bot_key_name='slack-bot', slack_app_key_name='slack-app'):
        vault = Vault()
        credentials = vault.read(vault_credentials_path)
        self.slack_bot_token = credentials[slack_bot_key_name]
        self.slack_app_token = credentials[slack_app_key_name]


    def create_headers(self):
        return {
            'Authorization': f'Bearer {self.slack_bot_token}',
        }


    def _get_params(self, **kwargs):
        base_dict = {}

        # Add any additional params passed as kwargs
        return {**base_dict, **kwargs}


    def lookup_user_by_email(self, email):
        url = os.path.join(SLACK_BASE_API, USER_LOOKUP_METHOD)
        headers = self.create_headers()
        params = self._get_params(email=email)

        r = requests.get(url, headers=headers, params=params)

        return r


    def open_conversation(self, user_list):
        url = os.path.join(SLACK_BASE_API, OPEN_CONVERSATION)
        headers = self.create_headers()

        users = ','.join(user_list)
        params = self._get_params(users=users)

        r = requests.post(url=url, headers=headers, params=params)

        return r


    def post_message(self, channel, text):
        url = os.path.join(SLACK_BASE_API, POST_MESSAGE_METHOD)
        headers = self.create_headers()
        data = self._get_params(channel=channel, text=text, headers=headers)

        r = requests.post(url=url, headers=headers, params=data)

        return r


    def delete_message(self, timestamp, channel_id):
        url = DELETE_MESSAGE_METHOD
        data = {
            'token': self.slack_bot_token,
            'ts': timestamp,
            'channel': channel_id
        }

        return requests.post(url=url, data=data)


    def lookup_and_send_user_message(self, user_email_list, message_text):
        user_ids = []
        for user_email in user_email_list:
            user_id = self.lookup_user_by_email(user_email).json()['user']['id']
            user_ids.append(user_id)
        conversation_id = self.open_conversation(user_ids).json()['channel']['id']

        r = self.post_message(conversation_id, message_text)

        return r


    def report_terminal_job_status(self, user_email_list, job_id, job_status):
        message_text = f"Hello! Your job {job_id} has completed with status {job_status}."

        self.lookup_and_send_user_message(user_email_list, message_text)
