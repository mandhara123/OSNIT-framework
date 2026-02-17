def score(text, keyword_dict):
    count = 0
    for words in keyword_dict.values():
        for w in words:
            if w in text:
                count += 1
    return count
