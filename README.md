# TempoMail is a asynchronous library to get temporary E-mails.

> Example:

```python
import asyncio

from TempoMail import RandomText, TempMail


async def main():
    username = RandomText(10)
    password = RandomText(8)
    # Use username and password if desired, otherwise: randomly generated.
    account = TempMail()  # set temp-mail information.
    async with account.session:
        # Create and Login to the temp-mail.
        domain = await account.get_domains_list()
        await account.login(username, password, domain)

        mail = await account.get_me()  # get temp-mail information

        print(f"Your Temp-Mail: {mail.address}\n\nWait for new message ...\n")

        without_msg = True
        while without_msg:
            async for message in account.get_messages():
                print(f"Subject: {message.subject}, text: {message.text}")
                without_msg = False  # break when first-message received

        # It's better to delete the user account after using it.
        await account.delete()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
```

### Installing

```bash
pip install TempoMail
```
