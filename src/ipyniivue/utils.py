"""
Important utilities needed to work data between Python and JavaScript code.

It includes a class to convert from snake to camel case as well as multiple
classes the serialize data to work with JS.
"""

import enum
import pathlib
import typing


def snake_to_camel(snake_str: str):
    """
    Convert the Python typical snake case to JS typical camel case.

    Parameters
    ----------
    snake_str : str
        The snake case string to be converted.

    Returns
    -------
    camel_string : str
        The parameter string converted to camel case.
    """
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def file_serializer(instance: typing.Union[pathlib.Path, str], widget: object):
    """
    Serialize a file to be transferred and read by the JS side.

    Parameters
    ----------
    instance : typing.Union[pathLib.Path, str]
        The path to a file to be serialized.
        Placeholder <fromfrontend> allowed for images added
        from the frontend.
    widget : object
        The NiiVue widget the instance is a part of.
    """
    if isinstance(instance, str):
        if instance == "<fromfrontend>":
            return {"name": "<fromfrontend>", "data": b""}
        # Make sure we have a pathlib.Path instance
        instance = pathlib.Path(instance)
    return {"name": instance.name, "data": instance.read_bytes()}


def serialize_options(instance: dict, widget: object):
    """
    Serialize the options for a NiiVue instance.

    Parameters
    ----------
    instance : dict
        The list of options to be serialized.
    widget : object
        The NiiVue widget the instance is a part of.
    """
    # Serialize enums as their value
    return {k: v.value if isinstance(v, enum.Enum) else v for k, v in instance.items()}
