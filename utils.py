from collections import Counter

def list_of_dict_stats(list_of_dict, key):
    return Counter(map(lambda x: x[key], list_of_dict))
