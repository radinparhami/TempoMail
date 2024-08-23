from TempoMail.client import TempoMail
from time import sleep

# Use username and password if desired, otherwise: randomly generated.
core = TempoMail(username=None, password=None)  # set temp-mail information.
# Create and Login to the temp-mail.
core.create()
core.authorize()

mail = core.get_account_info()  # get temp-mail information

print(mail)
print(f"\n\nYour Temp-Mail: {mail.address}\n\n")
print("Wait for new message ...")

first_msg = None
while not first_msg:
    sleep(1)
    messages = core.get_messages()
    for message in messages:
        print(f"Subject: {message.subject}, text: {message.text}")
        first_msg = message  # It continues until a new message is received

# It's better to delete the user account after using it.
core.delete_account()
