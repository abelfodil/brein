def filter_keys(old_dict: dict, keys: list[str]):
    return {key: old_dict[key] for key in set(keys).intersection(set(old_dict.keys()))}


def get_any_values(d: dict):
    return next(iter(d.values())) if d else None


def list_to_dict(l: list):
    return {str(i): e for i, e in enumerate(l)}


def recursive_get(obj: dict, keys: list[str]):
    stack = [obj]
    found_keys = set(keys)

    while stack:
        current_obj = stack.pop()

        if found_keys.intersection(current_obj.keys()):
            return current_obj[next(iter(found_keys.intersection(current_obj.keys())))]

        for value in current_obj.values():
            if isinstance(value, dict):
                stack.append(value)
            if isinstance(value, list):
                stack.extend(value)

    return None
