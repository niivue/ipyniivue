import numpy as np
import json

#these 2 functions are from https://github.com/martinRenou/ipycanvas/blob/master/ipycanvas/utils.py
#commands_to_buffer is slightly modified to remove the orjson dependency

def array_to_binary(ar):
    """Turn a NumPy array into a binary buffer."""
    # Unsupported int64 array JavaScript side
    if ar.dtype == np.int64:
        ar = ar.astype(np.int32)

    # Unsupported float16 array JavaScript side
    if ar.dtype == np.float16:
        ar = ar.astype(np.float32)

    # make sure it's contiguous
    if not ar.flags["C_CONTIGUOUS"]:
        ar = np.ascontiguousarray(ar)

    return {"shape": ar.shape, "dtype": str(ar.dtype)}, memoryview(ar)

def commands_to_buffer(commands):
    # Turn the commands list into a binary buffer
    return array_to_binary(
        np.frombuffer(bytes(json.dumps(commands), encoding="utf8"), dtype=np.uint8)
    )