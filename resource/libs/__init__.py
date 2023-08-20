import platform
import os
import data


def div():
    print("--------------------")


def br():
    div()
    input("Press ENTER to continue.")


def cls():
    """
    Clears the terminal screen.
    """
    res = platform.uname()
    os.system("cls" if res[0] == "Windows" else "clear")


def serialiseToDict(obj):
    """
    Custom JSON serializer for handling class instances and methods.
    """
    if isinstance(obj, types.FunctionType):
        return {"@itemType": "function", "code": obj.__code__.co_code.hex()}
    elif isinstance(obj, object) and hasattr(obj, "__dict__"):
        return {
            "@itemType": "class",
            "__module__": obj.__module__,
            "__class__": obj.__class__.__name__,
            **obj.__dict__,
        }
    return obj


def deserialiseFromDict(dct):
    """
    Custom JSON deserializer for handling class instances and methods.
    """
    if "@itemType" in dct:
        item_type = dct.pop("@itemType")
        if item_type == "function":
            method_code = bytes.fromhex(dct["code"])
            return types.FunctionType(code=method_code, globals=globals())
        elif item_type == "class":
            module_name = dct["__module__"]
            class_name = dct["__class__"]
            module = __import__(module_name)
            cls = getattr(module, class_name)
            instance = cls.__new__(cls)
            instance.__dict__.update(dct)
            return instance
    return dct


def objToDict(obj, addItemType=True):
    """
    Recursively convert an object and all its attributes to a dictionary.
    """
    if isinstance(obj, (int, float, bool, str)):
        return obj
    if inspect.isclass(obj):
        return {"__class__": obj.__name__}

    if isinstance(obj, (tuple, list)):
        return [obj_to_dict(x) for x in obj]

    if isinstance(obj, dict):
        if addItemType:
            obj2 = {"@itemType": type({}).__name__}
        obj2.update(obj)
        obj = obj2
        return {key: obj_to_dict(value) for key, value in obj.items()}
    obj_dict = {}
    if addItemType:
        obj_dict["@itemType"] = type(obj).__name__
    for attr in dir(obj):
        if attr.startswith("__") and attr.endswith("__"):
            continue
        if attr == "dic":
            continue
        value = getattr(obj, attr)
        obj_dict[attr] = obj_to_dict(value)
    return obj_dict
