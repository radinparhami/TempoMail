from datetime import datetime
from pprint import pformat


class Token:
    def __init__(self, token_update):
        # More info: https://docs.mail.tm/#authentication

        self.token: str = token_update.get("token")
        self.at_id: str = token_update.get("@id")
        self.id: str = token_update.get("id")

    def __repr__(self):
        return pformat(vars(self), indent=4, width=1)


class Account:
    def __init__(self, account_update):
        # More info: https://docs.mail.tm/#get-accountsid

        self.at_context: str = account_update.get("@context")
        self.at_id: str = account_update.get("@id")
        self.at_type: str = account_update.get("@type")
        self.id: str = account_update.get("id")
        self.address: str = account_update.get("address")
        self.quota: int = account_update.get("quota")
        self.used: int = account_update.get("used")
        self.is_disabled: bool = account_update.get("isDisabled")
        self.is_deleted: bool = account_update.get("isDeleted")
        self.created_at: datetime = datetime.fromisoformat(account_update.get("createdAt"))
        self.updated_at: datetime = datetime.fromisoformat(account_update.get("updatedAt"))

    def __repr__(self):
        return pformat(vars(self), indent=4, width=1)
