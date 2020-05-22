import os
import json
import random
from datetime import datetime
import time
import random

OUTPUT_FILE = "message_logs.txt"


MY_NAME = "NIRAL PATEL"
ACCOUNT_CREATION_YEAR = 2009
ACCOUNT_CREATION_MONTH = 10

ACCOUNT_CREATION_DATE = datetime(
    ACCOUNT_CREATION_YEAR,
    ACCOUNT_CREATION_MONTH,
    1
)

seen_initials = {}

ANONYMIZE = False  # set this to False to deanonymize friends


def anonymize(name):
    """
    returns initials for a name to anonymize it
    """
    
    if not ANONYMIZE:
        return name

    global seen_initials
    if name in seen_initials:
        return seen_initials[name]

    initials = "".join([p[0] for p in name.split(" ") if len(p) > 0])
    while initials in seen_initials.values():
        initials += str(random.choice(range(9)))

    seen_initials[name] = initials
    return initials


def convert_ms_to_months(time):
    message_date = datetime.fromtimestamp(time // 1000)
    return (message_date.year - ACCOUNT_CREATION_DATE.year) * 12 + message_date.month - ACCOUNT_CREATION_DATE.month


def process_dir(dir):
    for filename in os.listdir(dir):
        if filename.endswith(".json"):
            process_json_file(os.path.join(dir, filename))


def process_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        json_obj = json.load(f)  # read a conversation as a dictionary

    if len(json_obj['participants']) > 2:
        return 

    conversation_partner = anonymize(json_obj['participants'][0]['name'])

    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        for message in reversed(json_obj['messages']):
            if 'content' not in message:
                continue

            timestamp = convert_ms_to_months(message['timestamp_ms'])
            sender = message['sender_name']

            content = message['content'].lower()
            content = content.replace("\n", " ")
            content = content.replace("\r", "")
            content = content.replace("\t", " ")
            content = content.strip()

            if sender == MY_NAME:
                status = "sent"
            else:
                status = "received"

            f.write(f"{timestamp}\t{conversation_partner}\t{content}\t{status}\n")


def main():
    folders = [d for d in os.listdir() if os.path.isdir(d)
               and not d.startswith(".")]
    open(OUTPUT_FILE, 'w', encoding='utf-8').close()
    print("Reading data...")
    for dir in folders:
        process_dir(dir)


if __name__ == "__main__":
    main()
