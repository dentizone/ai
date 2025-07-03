from infisical_sdk import InfisicalSDKClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class InfisicalSecretManager:
    def __init__(self):
        self.client = InfisicalSDKClient(host=os.getenv("INFISICAL_HOST", "https://app.infisical.com"))
        self.client.auth.universal_auth.login(
            client_id=os.getenv("INFISICAL_CLIENT_ID"),
            client_secret=os.getenv("INFISICAL_CLIENT_SECRET")
        )
        self.project_id = os.getenv("INFISICAL_PROJECT_ID")
        self.environment_slug = os.getenv("INFISICAL_ENVIRONMENT_SLUG", "dev")
        self.secret_path = os.getenv("INFISICAL_SECRET_PATH", "/")

    def get_secret_value(self, key):
        secret = self.client.secrets.get_secret_by_name(
            secret_name=key,
            project_id=self.project_id,
            environment_slug=self.environment_slug,
            secret_path=self.secret_path,
            view_secret_value=True
        )
        # The property may be secret.secretValue or secret.value depending on SDK version
        return getattr(secret, 'secretValue', None) or getattr(secret, 'value', None)

def get_secret_value(key):
    manager = InfisicalSecretManager()
    return manager.get_secret_value(key)

