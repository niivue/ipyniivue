import enum
import pathlib
import typing


def snake_to_camel(snake_str: str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def file_serializer(instance: typing.Union[pathlib.Path, str], widget: object):
    if isinstance(instance, str):
        # make sure we have a pathlib.Path instance
        instance = pathlib.Path(instance)
    return {"name": instance.name, "data": instance.read_bytes()}


def mesh_layers_serializer(instance: list, widget: object):
    return [
        {**mesh_layer, "path": file_serializer(mesh_layer["path"], widget)}
        for mesh_layer in instance
    ]


def serialize_options(instance: dict, widget: object):
    # serialize enums as their value
    return {k: v.value if isinstance(v, enum.Enum) else v for k, v in instance.items()}
