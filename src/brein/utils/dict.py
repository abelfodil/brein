def filter_keys(old_dict: dict, keys: list[str]):
    return {key: old_dict[key] for key in set(keys).intersection(set(old_dict.keys()))}


def get_any_values(d: dict):
    return next(iter(d.values())) if d else None


def list_to_dict(l: list):
    return {str(i): e for i, e in enumerate(l)}


def recursive_get(obj: dict, keys: list[str]):
    if found_keys := set(keys).intersection(set(obj.keys())):
        return obj[next(iter(found_keys))]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = recursive_get(v, keys)
            if item is not None:
                return item
