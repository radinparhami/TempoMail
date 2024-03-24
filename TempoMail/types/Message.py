from datetime import datetime
from pprint import pformat


class Message:
    def __init__(self, message_update):
        # More info: https://docs.mail.tm/#get-messagesid

        self.at_context: str = message_update.get("@context")
        self.at_id: str = message_update.get("@id")
        self.at_type: str = message_update.get("@type")
        self.account_id: str = message_update.get("@id")

        self.bcc: list = message_update.get("bcc")
        self.cc: list = message_update.get("cc")

        self.download_url: str = message_update.get("downloadUrl")
        self.flagged: bool = message_update.get("flagged")
        self.has_attachment: bool = message_update.get("hasAttachment")
        self.html: list = message_update.get("html")
        self.id: str = message_update.get("id")
        self.intro: str = message_update.get("intro")
        self.is_deleted: bool = message_update.get("isDeleted")
        self.message_id: str = message_update.get("msgid")
        self.retention: bool = message_update.get("retention")
        self.retention_date: datetime = datetime.fromisoformat(message_update.get("retentionDate"))
        self.seen: bool = message_update.get("seen")
        self.size: int = message_update.get("size")
        self.source_url: str = message_update.get("sourceUrl")

        self.subject: str = message_update.get("subject")
        self.text: str = message_update.get("text")

        self.from_user: dict = message_update.get("from")
        self.to: dict = message_update.get("to")

        self.created_at: datetime = datetime.fromisoformat(message_update.get("createdAt"))
        self.updated_at: datetime = datetime.fromisoformat(message_update.get("updatedAt"))

        self.verifications: dict = message_update.get("verifications")

    def __repr__(self):
        return pformat(vars(self), indent=4, width=1)
