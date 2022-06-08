""" API for the pump """
import asyncio

from db import schemas
import json, time
try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources  # python <3.7


def set_busy(value: bool) -> None:
    """ Set the busy state """
    state = {"busy": value}
    with pkg_resources.path('pump', "state.json") as path:
        with open(path, "w") as f:
            json.dump(state, f)


async def make_recipe(recipe: schemas.Recipe) -> None:
    """ Make a cocktail """
    set_busy(True)
    print(recipe)
    await asyncio.sleep(5)
    set_busy(False)


def busy() -> bool:
    """ Check if pump is busy """
    with pkg_resources.path('pump', "state.json") as path:
        with open(path, "r") as f:
            state = json.load(f)
    return state["busy"]
