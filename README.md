# TempoMail
python temp-mail liberary

## for install
`pip install TempoMail`

## Example of creating and receiving email using TempoMail:
```python
from time import sleep

from TempoMail.client import TempoMail

# Use username and password if desired, otherwise: randomly generated.
core = TempoMail(username=None, password=None)  # set temp-mail information.
core.create(), core.authorize()  # Create and Login to the temp-mail.

mail = core.get_account_info()  # get temp-mail information

print(mail)
print(f"\n\nYour Temp-Mail: {mail.address}\n\n")
print("Wait for new message ...")

while True:
    sleep(1)
    messages = core.get_messages()
    if core.get_messages():
        for message in messages:
            print(f"Subject: {message.subject}, text: {message.text}")

        if messages:
            break  # It continues until a new message is received

# It's better to delete the user account after using it.
core.delete_account()

```