from collections import Counter
from datetime import datetime
from utils import load_json
from string import punctuation


def count_users_messages():
    users = load_json("./src/data/users.json")
    
    usernames = {}
    for user in users.values():
        if "username" in user:
            usernames[user["id"]] = user["username"] 
            continue

        usernames[user["id"]] = user["first_name"]

    total = Counter(dict())
    messages = load_json("./src/data/database.json")
    for message in messages:
        message["time"] = datetime.fromtimestamp(message["time"])
        message["from"] = usernames[message["from"]]
        message["to"] = usernames[message["to"]]

        total[message["from"]] += 1
        

    print(total.most_common())
    print(len(total))



def count_users_words():
    messages = load_json("./src/data/database.json")

    words = Counter(dict())
    for message in messages:
        text = message["text"]
        text = text.lower()
        for p in punctuation:
            text = text.replace(p, " ")

        for word in text.split():
            words[word] += 1


    print(words.most_common())
    print(len(words))
        

def main():
    # count_users_words()
    count_users_messages()



if __name__ == "__main__":
    main()