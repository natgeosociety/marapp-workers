import os
from functools import reduce
from posixpath import join


def deepgetattr(obj, attr, default=None, sep="."):
    """Recurse through an attribute chain to get the ultimate value."""

    return reduce(lambda o, key: o.get(key, default), attr.split(sep), obj)


def required_keys(obj, keys, sentinel=object()):
    """
    Validates keys value at path of object.
    """
    missing_keys = list(filter(lambda k: deepgetattr(obj, k, sentinel) == sentinel, keys))

    if len(missing_keys):
        raise ValueError(f"Required parameters: {', '.join(missing_keys)}")


def filesizeformat(bytes_):
    """
    Format the value like a 'human-readable' file size (i.e. 13 KB, 4.1 MB,
    102 bytes, etc.).
    """
    try:
        bytes_ = int(bytes_)
    except (TypeError, ValueError, UnicodeDecodeError):
        value = "{} bytes".format(0)
        return value

    def number_format(number):
        return round(number, 1)

    KB = 1 << 10
    MB = 1 << 20
    GB = 1 << 30
    TB = 1 << 40
    PB = 1 << 50

    negative = bytes_ < 0
    if negative:
        bytes_ = -bytes_  # Allow formatting of negative numbers.

    if bytes_ < KB:
        value = "{} bytes".format(bytes_)
    elif bytes_ < MB:
        value = "{} KB".format(number_format(bytes_ / KB))
    elif bytes_ < GB:
        value = "{} MB".format(number_format(bytes_ / MB))
    elif bytes_ < TB:
        value = "{} GB".format(number_format(bytes_ / GB))
    elif bytes_ < PB:
        value = "{} TB".format(number_format(bytes_ / TB))
    else:
        value = "{} PB".format(number_format(bytes_ / PB))

    if negative:
        value = "-{}".format(value)
    return value


def urljoin(base, *args):
    """Join all arguments together and normalize the resulting URL"""

    parts = [part.strip("/") for part in args if part]
    return join(base, *parts)


def abspath(current_path, relative_path):
    """Build an absolute path from relative path"""

    parent = os.path.abspath(os.path.dirname(current_path))
    return os.path.join(parent, relative_path)
