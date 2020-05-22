import string

DATA_FILENAME = "message_logs.txt"


def add_one_to_count(counts, counted, month):
    if counted not in counts:
        counts[counted] = {}
    inner_counts = counts[counted]
    if month not in inner_counts:
        inner_counts[month] = 0
    inner_counts[month] += 1
    return counts


def get_counts_per_person():
    """
    Return a dict from friend's names to dicts from months to
    message counts
    """
    counts = {}  # initialize a counts dict
    with open(DATA_FILENAME, 'r') as f:
        for line in f:
            line_parts = line.split('\t')
            month = int(line_parts[0])
            conversation_partner = line_parts[1]

            counts = add_one_to_count(counts, conversation_partner, month)

    return counts


def get_chat_word_counts():
    """
    Return a dict from words to dicts from months to
    counts of word usage per month
    """
    counts = {}  # initialize a counts dict
    with open(DATA_FILENAME, 'r') as f:
        for line in f:
            # turn a line into a list of constituent parts,
            # and yank out the relevant bit
            line_parts = line.split('\t')
            month = int(line_parts[0])
            content = without_punctuation(line_parts[2].lower())
            status = line_parts[3]

            if status == "received":
                # only considering messages that I sent
                # so if we find one that I received, move on
                continue

            # return a list of individual words in the message
            words = content.split()

            for word in words:
                counts = add_one_to_count(counts, word, month)

    return counts


def get_last_chat_month():
    """
    return the largest month in the file, which we'll
    use as a proxy for the age of your facebook account
    (assumes you've used facebook in the last month.)
    """
    with open(DATA_FILENAME, 'r') as f:
        lines = f.readlines()

    # turn lines into a list of length-4 lists
    lines = [line.split("\t") for line in lines]
    # uses list comprehension to get back
    # just the months from each line
    months = [int(line[0]) for line in lines]
    return max(months)


def without_punctuation(s):
    """
    Strip punctuation from a given string
    """
    for punc in string.punctuation:
        s = s.replace(punc, "")
    return s
