# TEMP-MAIL
# base reference: https://docs.mail.tm/

from typing import List

from .types import Account, Message
from .core import Mail, __send_request__


class TempoMail(Mail):
    def get_messages(self, page: int = 1) -> List[Message]:
        result = __send_request__(
            "messages", args=dict(page=page),
            head=self.auth_head_gen
        )
        for msg_data in result.get("hydra:member"):
            # recover the full message
            msg_result: Message = Message(__send_request__(
                ["messages", msg_data['id']],
                head=self.auth_head_gen
            ))

            yield msg_result

    def get_account_info(self) -> Account:
        return Account(self.__action__())

    def delete_account(self) -> bool:
        return self.__action__("DELETE")
