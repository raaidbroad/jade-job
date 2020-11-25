# accessing vault keys
import hvac

# filesystem/env variables support
import os


class Vault:
    VAULT_ADDR = os.environ['VAULT_ADDR']

    def __init__(self):
        self.client = hvac.Client(url=self.VAULT_ADDR, token=self._token())

    def read(self, path):
        return self.client.read(path).get('data')

    # private methods

    def _token(self):
        # try the environment variable
        env_token = os.environ.get("VAULT_TOKEN")
        if env_token is not None:
            return env_token

        # look for the .vault-token file in the home directory
        # n.b.: vault also searches for the token by recursively scanning up from the working directory.
        #       this feels like too much effort for now, but can be added if it ends up being a problem.
        token_path = os.path.expanduser("~/.vault-token")
        if os.path.isfile(token_path):
            with open(token_path) as vault_token_file:
                return vault_token_file.read().rstrip()

        raise ValueError("Couldn't find a vault token. Looked in the VAULT_TOKEN environment variable and in ~/.vault-token")
