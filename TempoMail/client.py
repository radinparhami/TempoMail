# TEMP-MAIL
# base reference: https://docs.mail.tm/


from .core import MailCenter
from .types import Account, Message


class TempMail(MailCenter):
    async def get_messages(self, page: int = 1):
        _, result = await self._send_request(
            f"/messages?page={page}", head=self.authenticate
        )
        for msg_data in result.get(self._MASTER_KEY, []):
            # recover the full message
            _, result = await self._send_request(
                ["/messages", msg_data["id"]], head=self.authenticate
            )

            yield Message(result)

    async def get_me(self) -> Account:
        _, result = await self._action("GET")
        return Account(result)

    async def delete(self):
        status, _ = await self._action("GET")
        return status == 204
