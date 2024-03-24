# TEMP-MAIL
# base reference: https://docs.mail.tm/

from json import dumps
from pprint import pprint
from random import choices, choice
from string import ascii_lowercase, digits
from typing import Union, List

import requests

from .types import Token

api_address = "https://api.mail.tm/"
chars = ascii_lowercase + digits + "._"
generate_chars = (lambda length: ''.join(choices(chars, k=length)))


def __send_request__(
        end_point: Union[List[str], str], method: str = "GET",
        head: dict = None, args: dict = None, data: dict = None,
        except_status_codes: Union[List[int], int] = None,
) -> Union[requests.Response, int, False]:
    end_points: str = end_point if not isinstance(end_point, list) else "/".join(end_point)
    url = api_address + (end_points[1:] if end_points.startswith("/") else end_points)
    except_status_codes = except_status_codes if isinstance(except_status_codes, list) else [except_status_codes]
    if args:
        url += '?' + '&'.join([f'{k}={v}' for k, v in args.items()])
    headers = {
        "accept": "application/ld+json",
        "Content-Type": "application/json",
    }
    response = requests.request(
        method=method.lower(), url=url,
        headers={**headers, **head} if head else headers,
        data=data and dumps(data),
    )
    if response.status_code not in (200, 201, *except_status_codes):
        print(f"Error {response.status_code}:")
        pprint(response.json())
        return False

    return response.text and response.json() or response.status_code


class Mail:
    def __init__(self, username: str = None, password: str = None, domain: str = None):
        self.username = username or generate_chars(16)
        self.password = password or generate_chars(6)
        self.domain = domain or choice(self.get_domains_list)

        self.token_info = None

        self.email_address = "{username}@{domain}".format(
            username=self.username,
            domain=self.domain
        )

    @property
    def get_domains_list(self) -> Union[List[str], None]:
        result = __send_request__('domains')
        if result and result.get("hydra:member"):
            return list(map(lambda x: x["domain"], result["hydra:member"]))

    def create(self, end_point: str = "accounts") -> Union[dict, None]:
        return __send_request__(
            end_point=end_point, method="POST",
            data=dict(
                address=self.email_address,
                password=self.password,
            )
        )

    def authorize(self):
        self.token_info: Token = Token(self.token_info or self.create(end_point="token"))

    @property
    def token(self) -> Token:
        if self.token_info:
            return self.token_info
        print("ERROR you must login first! Use `authorize` method."), exit()

    @property
    def auth_head_gen(self):
        return dict(Authorization=f"Bearer {self.token.token}")

    def __action__(self, action: str = "get") -> Union[bool, dict]:
        if not action.lower() in ["get", "delete"]:
            print("ERROR: invalid action")
            return False
        is_delete = action.lower() == "delete"
        result: dict = __send_request__(
            end_point=self.token.at_id, method=action,
            head=self.auth_head_gen, except_status_codes=[204, 401]
        )

        return is_delete and 204 == result or result
