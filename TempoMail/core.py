# TEMP-MAIL
# base reference: https://docs.mail.tm/

from json import dumps
from random import choice, choices
from string import ascii_lowercase, digits
from typing import Dict, List, Tuple, Union

from aiohttp import ClientSession

from .types import Token


class RandomText:
    _chars = ascii_lowercase + digits + "_"

    def __init__(self, length: int) -> None:
        self.length = length

    def generate(self) -> str:
        return "".join(choices(self._chars, k=self.length))


class MailCenter:
    _API_ADDRESS: str = "https://api.mail.tm"
    _HEADERS: Dict[str, str] = {
        "accept": "application/ld+json",
        "Content-Type": "application/json",
    }
    _MASTER_KEY: str = "hydra:member"

    def __init__(
        self,
        session: Union[ClientSession, None] = None,
    ):
        self.session = session or ClientSession()
        self._token_info: Union[Token, None] = None

    async def _send_request(
        self,
        end_point: Union[List[str], str],
        method: str = "GET",
        head: Union[dict, None] = None,
        data: Union[dict, None] = None,
    ) -> Tuple[int, dict]:
        end_points: str = "/".join(
            [end_point]
            if isinstance(
                end_point,
                str,
            )
            else end_point
        )

        response = await self.session.request(
            method=method.lower(),
            url=self._API_ADDRESS + end_points,
            # add customize headers
            headers={**self._HEADERS, **head} if head else self._HEADERS,
            data=data and dumps(data),
        )
        if response.status not in [200, 201, 204]:
            # print(f"Error {response.status_code}:")
            # pprint(response.json())
            return response.status, {}
        elif response.method == "DELETE":
            return response.status, {}

        return response.status, await response.json()

    async def get_domains_list(self) -> List[str]:
        _, result = await self._send_request("/domains")
        if result.get(self._MASTER_KEY):
            return list(map(lambda x: x["domain"], result[self._MASTER_KEY]))
        else:
            print("ERROR to find domain!")
            exit()

    async def _create(self, end_point: str):
        return await self._send_request(
            end_point=end_point,
            method="POST",
            data=dict(
                address=self.email_address,
                password=self.password,
            ),
        )

    async def login(
        self,
        username: Union[str, RandomText],
        password: Union[str, RandomText],
        domain: Union[str, List[str]],
    ):
        if isinstance(username, RandomText):
            username = username.generate()
        if isinstance(password, RandomText):
            password = password.generate()
        if isinstance(domain, list):  # select randomly
            domain = choice(domain)

        self.username: str = username
        self.password: str = password
        self.domain: str = domain
        self.email_address = "{username}@{domain}".format(
            username=self.username, domain=self.domain
        )
        await self._create(end_point="/accounts")  # Create Account

        if self._token_info is None:
            status, result = await self._create(end_point="/token")
            self._token_info = Token(result)
            if status == 401:
                print(
                    f"username: {username} is invalid! (remove dot or unknown characters from username)"
                )
                exit()

        return self._token_info

    @property
    def token(self) -> Token:
        if not self._token_info:
            print("ERROR you must login first! Use `login` method.")
            exit()
        return self._token_info

    @property
    def authenticate(self):
        return {"Authorization": f"Bearer {self.token.token}"}

    async def _action(self, action) -> Tuple[int, dict]:
        if action.upper() not in ["GET", "DELETE"]:
            print("ERROR: invalid action")
            return (500, {})

        status, result = await self._send_request(
            end_point=self.token.at_id,
            method=action,
            head=self.authenticate,
        )

        return status, result
