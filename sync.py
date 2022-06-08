import time
from datetime import datetime
from pprint import pprint
from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.schemas import (
    BibCreate,
    UserCreate,
    RecipeCreate,
    IngredientCreate,
    ImageCreate,
)
from utils import diff, as_dict, dict_in_list
from base64 import b64encode
import os, requests
from itertools import cycle
from shutil import get_terminal_size
from colorama import Fore, Style
from threading import Thread


class Loader:
    def __init__(self, desc="Loading...", timeout=0.3):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        # self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.steps = ["[|]", "[/]", "[-]", "[\\]", "[|]", "[/]", "[-]", "[\\]"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{Fore.GREEN}{c} {Fore.WHITE}{self.desc} ", flush=True, end="")
            time.sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self, end="Done !"):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print(Style.RESET_ALL + "\r" + " " * cols, end="", flush=True)
        print(f"\r{end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


# ----------------------------------------------------------------------------------------------------------------------


class SyncDependencyException(Exception):
    """Used for dependency sync dependency calculations"""

    pass


# ---------------------------------------------------------------------------------------------------------------------


def mock_sync_bibs(db):
    """Sync bibs from the distant database to the local db."""
    local_bibs = list(map(as_dict, crud.get_bibs(db)))
    mock_distant_bibs = [
        {"id": 1, "name": "rhum blanc", "alcool": True},
        {"id": 2, "name": "rhum ambré", "alcool": True},
        {"id": 3, "name": "tequila", "alcool": True},
        {"id": 4, "name": "grand marnier", "alcool": True},
        {"id": 5, "name": "vodka", "alcool": True},
        {"id": 6, "name": "cognac", "alcool": True},
        {"id": 7, "name": "jus de citron", "alcool": False},
        {"id": 8, "name": "jus de citron vert", "alcool": False},
        {"id": 9, "name": "jus de cranberry", "alcool": False},
        {"id": 10, "name": "curaçao bleu", "alcool": True},
        {"id": 11, "name": "sirop de menthe", "alcool": False},
        {"id": 12, "name": "sirop de sucre de canne", "alcool": False},
        {"id": 13, "name": "sirop de melon", "alcool": False},
        {"id": 14, "name": "eau gazeuse", "alcool": False},
        {"id": 15, "name": "jus d'orange", "alcool": False},
        {"id": 16, "name": "jus d'ananas", "alcool": False},
        {"id": 17, "name": "lait de coco", "alcool": False},
        {"id": 18, "name": "crème de pêche", "alcool": True},
    ]

    delete_count = 0
    for local_bib in local_bibs:
        if local_bib["id"] not in [bib["id"] for bib in mock_distant_bibs]:
            crud.delete_bib(db, local_bib["id"])
            delete_count += 1
    add_count = 0
    for local_bib in mock_distant_bibs:
        if local_bib["id"] not in [bib["id"] for bib in local_bibs]:
            crud.create_bib(db, BibCreate(**local_bib))
            add_count += 1
    if os.environ["VERBOSE"] == "true":
        print(f"deleted {delete_count} bib(s), added {add_count} bib(s)")


def mock_sync_users(db):
    """Sync users from the distant database to the local db."""
    local_users = list(map(as_dict, crud.get_users(db)))
    mock_distant_users = [{"id": 1, "name": "Cocktail.me", "role": "admin"}]
    delete_count = 0
    for local_user in local_users:
        if local_user["id"] not in [user["id"] for user in mock_distant_users]:
            crud.delete_user(db, local_user["id"])
            delete_count += 1
    add_count = 0
    for local_user in mock_distant_users:
        if local_user["id"] not in [user["id"] for user in local_users]:
            crud.create_user(db, UserCreate(**local_user))
            add_count += 1
    if os.environ["VERBOSE"] == "true":
        print(f"deleted {delete_count} user(s), added {add_count} user(s)")


def mock_sync_recipes(db):
    """Sync recipes from the distant database to the local db."""
    local_recipes = list(map(as_dict, crud.get_recipes(db)))
    mock_distant_recipes = [
        {
            "id": 1,
            "title": "Mojito",
            "description": "mojito",
            "author_id": 1,
            "price": 5,
        },
        {"id": 2, "title": "Punch", "description": "punch", "author_id": 1, "price": 5},
        {
            "id": 3,
            "title": "Piña colada",
            "description": "piña colada",
            "author_id": 1,
            "price": 5,
        },
        {
            "id": 4,
            "title": "Margarita",
            "description": "margarita",
            "author_id": 1,
            "price": 5,
        },
        {
            "id": 5,
            "title": "Cosmopolitan",
            "description": "cosmopolitan",
            "author_id": 1,
            "price": 5,
        },
        {
            "id": 6,
            "title": "Blue Lagoon",
            "description": "blue lagoon",
            "author_id": 1,
            "price": 5,
        },
        {
            "id": 7,
            "title": "Sex on the beach",
            "description": "sex on the beach",
            "author_id": 1,
            "price": 5,
        },
        {
            "id": 8,
            "title": "Jus d'orange",
            "description": "jus d'orange",
            "author_id": 1,
            "price": 3,
        },
        {
            "id": 9,
            "title": "Diabolo Menthe",
            "description": "diabolo menthe",
            "author_id": 1,
            "price": 3,
        },
    ]
    delete_count = 0
    for local_recipe in local_recipes:
        if local_recipe["id"] not in [recipe["id"] for recipe in mock_distant_recipes]:
            crud.delete_recipe(db, local_recipe["id"])
            delete_count += 1
    add_count = 0
    for recipe in mock_distant_recipes:
        if recipe["id"] not in [local_recipe["id"] for local_recipe in local_recipes]:
            crud.create_recipe(db, RecipeCreate(**recipe))
            add_count += 1
    if os.environ["VERBOSE"] == "true":
        print(f"deleted {delete_count} recipe(s), added {add_count} recipe(s)")


def mock_sync_ingredients(db):
    """Sync ingredients from the distant database to the local db."""
    local_ingredients = list(map(as_dict, crud.get_ingredients(db)))
    mock_distant_ingredients = [
        {"recipe_id": 1, "bib_id": 1, "amount": 60},
        {"recipe_id": 1, "bib_id": 14, "amount": 200},
        {"recipe_id": 1, "bib_id": 8, "amount": 30},
        {"recipe_id": 1, "bib_id": 12, "amount": 20},
        {"recipe_id": 2, "bib_id": 1, "amount": 100},
        {"recipe_id": 2, "bib_id": 12, "amount": 50},
        {"recipe_id": 2, "bib_id": 15, "amount": 100},
        {"recipe_id": 2, "bib_id": 16, "amount": 100},
        {"recipe_id": 3, "bib_id": 1, "amount": 40},
        {"recipe_id": 3, "bib_id": 2, "amount": 20},
        {"recipe_id": 3, "bib_id": 16, "amount": 120},
        {"recipe_id": 3, "bib_id": 17, "amount": 40},
        {"recipe_id": 4, "bib_id": 3, "amount": 50},
        {"recipe_id": 4, "bib_id": 4, "amount": 30},
        {"recipe_id": 4, "bib_id": 8, "amount": 20},
        {"recipe_id": 5, "bib_id": 5, "amount": 40},
        {"recipe_id": 5, "bib_id": 4, "amount": 20},
        {"recipe_id": 5, "bib_id": 9, "amount": 20},
        {"recipe_id": 5, "bib_id": 8, "amount": 10},
        {"recipe_id": 6, "bib_id": 5, "amount": 40},
        {"recipe_id": 6, "bib_id": 10, "amount": 30},
        {"recipe_id": 6, "bib_id": 7, "amount": 20},
        {"recipe_id": 7, "bib_id": 5, "amount": 30},
        {"recipe_id": 7, "bib_id": 16, "amount": 50},
        {"recipe_id": 7, "bib_id": 9, "amount": 60},
        {"recipe_id": 7, "bib_id": 18, "amount": 10},
        {"recipe_id": 8, "bib_id": 15, "amount": 200},
        {"recipe_id": 9, "bib_id": 14, "amount": 180},
        {"recipe_id": 9, "bib_id": 11, "amount": 20},
    ]
    delete_count = 0
    for local_ingredient in local_ingredients:
        if (local_ingredient["recipe_id"], local_ingredient["bib_id"]) not in [
            (ingredient["recipe_id"], ingredient["bib_id"])
            for ingredient in mock_distant_ingredients
        ]:
            crud.delete_ingredient(db, local_ingredient["id"])
            delete_count += 1
    add_count = 0
    for ingredient in mock_distant_ingredients:
        if (ingredient["recipe_id"], ingredient["bib_id"]) not in [
            (local_ingredient["recipe_id"], local_ingredient["bib_id"])
            for local_ingredient in local_ingredients
        ]:
            crud.create_ingredient(db, IngredientCreate(**ingredient))
            add_count += 1
    if os.environ["VERBOSE"] == "true":
        print(f"deleted {delete_count} ingredient(s), added {add_count} ingredient(s)")


def mock_sync_images(db):
    """Sync images from the distant database to the local db."""
    local_images = list(map(as_dict, crud.get_images(db)))
    mock_distant_images = []
    for filename in os.listdir("mock/images"):
        with open("mock/images/" + filename, "rb") as file:
            mock_distant_images.append(
                {
                    "id": int(filename.split(".")[0]),
                    "recipe_id": filename.split(".")[0],
                    "data": b64encode(file.read()),
                }
            )
    delete_count = 0
    for local_image in local_images:
        if local_image["id"] not in [image["id"] for image in mock_distant_images]:
            crud.delete_image(db, local_image["id"])
            delete_count += 1
    add_count = 0
    for image in mock_distant_images:
        if image["id"] not in [local_image["id"] for local_image in local_images]:
            crud.create_image(db, ImageCreate(**image))
            add_count += 1
    if os.environ["VERBOSE"] == "true":
        print(f"deleted {delete_count} image(s), added {add_count} image(s)")


def mock_sync_orders(db):
    """Sync orders from the local database to the distant db."""
    local_orders = list(map(as_dict, crud.get_orders(db)))
    mock_distant_orders = []
    if os.environ["VERBOSE"] == "true":
        print(f"sent {len(local_orders)} new order(s)")
    for order in local_orders:
        mock_distant_orders.append(order)
        crud.delete_order(db, order["id"])


def mock_sync_loaded_bibs(db):
    """Add loaded bibs to the local database, for test purposes."""
    local_loaded_bibs = list(map(as_dict, crud.get_loaded_bibs(db)))
    mock_distant_loaded_bibs = [
        {"bib_id": 4, "amount": 3000},
        {"bib_id": 11, "amount": 3000},
        {"bib_id": 5, "amount": 3000},
        {"bib_id": 12, "amount": 3000},
        {"bib_id": 1, "amount": 3000},
        {"bib_id": 2, "amount": 3000},
        {"bib_id": 3, "amount": 3000},
    ]
    delete_count = 0
    for local_loaded_bib in local_loaded_bibs:
        if local_loaded_bib["bib_id"] not in [
            loaded_bib["bib_id"] for loaded_bib in mock_distant_loaded_bibs
        ]:
            crud.delete_loaded_bib(db, local_loaded_bib["id"])
            delete_count += 1
    add_count = 0
    for loaded_bib in mock_distant_loaded_bibs:
        if loaded_bib["bib_id"] not in [
            local_loaded_bib["bib_id"] for local_loaded_bib in local_loaded_bibs
        ]:
            crud.create_loaded_bib(db, **loaded_bib)
            add_count += 1
    if os.environ["VERBOSE"] == "true":
        print(f"deleted {delete_count} loaded_bib(s), added {add_count} loaded_bib(s)")


# ---------------------------------------------------------------------------------------------------------------------


def sync_bibs(db):
    """Sync bibs from the distant database to the local db."""
    loader = Loader(
        desc="Syncing bibs...",
    ).start()
    local_bibs = list(map(as_dict, crud.get_bibs(db)))
    distant_bibs = requests.get(os.environ["DISTANT_API_URL"] + "/bibTypes").json()[
        "content"
    ]
    for bib in distant_bibs:
        del bib["price"]

    deleted = 0
    added = 0
    for l_bib in local_bibs:
        if not dict_in_list(l_bib, distant_bibs):
            crud.delete_bib(db, l_bib["id"])
            deleted += 1
    for d_bib in distant_bibs:
        if not dict_in_list(d_bib, local_bibs):
            crud.create_bib(db, BibCreate(**d_bib))
            added += 1
    loader.stop(
        end=f"[{Fore.GREEN}✓{Style.RESET_ALL}] Added {Fore.GREEN}{added}{Style.RESET_ALL}"
        + f" and deleted {Fore.RED}{deleted}{Style.RESET_ALL} users."
    )


def sync_users(db):
    """Sync users from the distant database to the local db."""
    loader = Loader(
        desc="Syncing users...",
    ).start()
    local_users = list(map(as_dict, crud.get_users(db)))
    distant_users = requests.get(os.environ["DISTANT_API_URL"] + "/accounts").json()[
        "content"
    ]
    for user in distant_users:
        del user["hash"]
        del user["lastModified"]
        del user["email"]
    deleted = 0
    for l_user in local_users:
        if not dict_in_list(l_user, distant_users):
            crud.delete_user(db, l_user["id"])
            deleted += 1
    added = 0
    for d_user in distant_users:
        if not dict_in_list(d_user, local_users):
            crud.create_user(db, UserCreate(**d_user))
            added += 1

    loader.stop(
        end=f"[{Fore.GREEN}✓{Style.RESET_ALL}] Added {Fore.GREEN}{added}{Style.RESET_ALL}"
        + f" and deleted {Fore.RED}{deleted}{Style.RESET_ALL} users."
    )


def sync_recipes(db):
    """Sync recipes from the distant database to the local db."""
    loader = Loader(desc="Syncing recipes").start()
    local_recipes = list(map(as_dict, crud.get_recipes(db)))
    distant_recipes = requests.get(os.environ["DISTANT_API_URL"] + "/recipes").json()[
        "content"
    ]
    for recipe in distant_recipes:
        del recipe["voteNumber"]
        del recipe["voteResult"]
        del recipe["ingredients"]
        del recipe["picture"]
        del recipe["listIngredients"]
        recipe["title"] = recipe["name"]
        del recipe["name"]
        recipe["author_id"] = recipe["author"]["id"]
        del recipe["author"]
        del recipe["date"]
        del recipe["alcool"]

    for recipe in local_recipes:
        del recipe["author"]
        del recipe["ingredients"]
        del recipe["image"]

    new_distant_recipes = []
    for recipe in distant_recipes:
        new_distant_recipes.append(recipe)
    distant_recipes = new_distant_recipes

    deleted = 0
    added = 0
    for l_recipe in local_recipes:
        if not dict_in_list(l_recipe, distant_recipes):
            crud.delete_recipe(db, l_recipe["id"])
            deleted += 1

    for d_recipe in distant_recipes:
        if not dict_in_list(d_recipe, local_recipes):
            crud.create_recipe(db, RecipeCreate(**d_recipe))
            added += 1
    loader.stop(
        end=f"[{Fore.GREEN}✓{Style.RESET_ALL}] Added {Fore.GREEN}{added}{Style.RESET_ALL}"
        + f" and deleted {Fore.RED}{deleted}{Style.RESET_ALL} recipes."
    )


def sync_ingredients(db):
    """Sync ingredients from the distant database to the local db."""
    loader = Loader(desc="Syncing ingredients...").start()
    local_ingredients = list(map(as_dict, crud.get_ingredients(db)))
    distant_recipes = requests.get(os.environ["DISTANT_API_URL"] + "/recipes").json()[
        "content"
    ]
    distant_ingredients = []
    for d_rec in distant_recipes:
        for ingredient in d_rec["ingredients"]:
            distant_ingredients.append(
                {
                    "recipe_id": d_rec["id"],
                    "bib_id": ingredient["bibType"]["id"],
                    "amount": ingredient["quantity"],
                }
            )
    for ingredient in local_ingredients:
        del ingredient["bib"]
    deleted = 0
    added = 0
    for l_ingredient in local_ingredients:
        if not dict_in_list(l_ingredient, distant_ingredients):
            crud.delete_ingredient(
                db, l_ingredient["recipe_id"], l_ingredient["bib_id"]
            )
            deleted += 1

    for d_ingredient in distant_ingredients:
        if not dict_in_list(d_ingredient, local_ingredients):
            crud.create_ingredient(db, IngredientCreate(**d_ingredient))
            added += 1

    loader.stop(
        end=f"[{Fore.GREEN}✓{Style.RESET_ALL}] Added {Fore.GREEN}{added}{Style.RESET_ALL}"
        + f" and deleted {Fore.RED}{deleted}{Style.RESET_ALL} ingredients."
    )


def sync_images(db):
    """Sync images from the distant database to the local db."""
    loader = Loader(desc="Syncing images...").start()
    local_images = list(map(as_dict, crud.get_images(db)))
    for local_image in local_images:
        del local_image["id"]
    distant_recipes = requests.get(os.environ["DISTANT_API_URL"] + "/recipes").json()[
        "content"
    ]
    distant_images = [
        {
            "recipe_id": recipe["id"],
            "data": requests.get(
                os.environ["DISTANT_API_URL"] + "/recipe/" + recipe["id"]
            )["content"],
        }
        for recipe in distant_recipes
        if recipe["picture"]
    ]
    deleted = 0
    added = 0
    for l_image in local_images:
        if not dict_in_list(l_image, distant_images):
            crud.delete_image(db, l_image["recipe_id"])
            deleted += 1
    for d_image in distant_images:
        if not dict_in_list(d_image, local_images):
            crud.create_image(db, ImageCreate(**d_image))
            added += 1
    loader.stop(
        end=f"[{Fore.GREEN}✓{Style.RESET_ALL}] Added {Fore.GREEN}{added}{Style.RESET_ALL}"
        + f" and deleted {Fore.RED}{deleted}{Style.RESET_ALL} images."
    )


def sync_orders(db):
    """Sync orders from the local database to the distant db."""
    local_orders = list(map(as_dict, crud.get_orders(db)))
    for order in local_orders:
        requests.post(
            os.environ["DISTANT_API_URL"] + "/purchaseOrders",
            json={
                "consumerId": order["consumer_id"],
                "date": order["date"],
                "machineSerial": os.environ["MACHINE_ID"],
                "recipeId": order["recipe_id"],
            },
        )
        crud.delete_order(db, order["id"])


def sync_loaded_bibs(db):
    """Sync loaded bibs from server."""
    # TODO: regarder s'il existe des unloaded_bibs pour deviner si on doit
    #  lire du serveur ou écrire dans le serveur
    local_loaded_bibs = list(map(as_dict, crud.get_loaded_bibs(db)))
    distant_loaded_bibs = requests.get(
        os.environ["DISTANT_API_URL"] + "/machines?serial=" + os.environ["MACHINE_ID"]
    ).json()["content"]["bibs"]
    new_distant_loaded_bibs = []
    for distant_loaded_bib in distant_loaded_bibs:
        new_distant_loaded_bibs.append(
            {
                "id": distant_loaded_bib["id"],
                "bib_id": distant_loaded_bib["type"]["id"],
                "amount": distant_loaded_bib["quantity"],
            }
        )
    old_distant_loaded_bibs = distant_loaded_bibs
    distant_loaded_bibs = new_distant_loaded_bibs
    sent = 0
    downloaded = 0
    for l_loaded_bib in local_loaded_bibs:
        if not dict_in_list(l_loaded_bib, distant_loaded_bibs):
            requests.post(
                os.environ["DISTANT_API_URL"] + "/loadedBibs",
                json={
                    "serial": os.environ["MACHINE_ID"],
                    "dto": {"bibs": [distant_loaded_bibs]},
                },
            )
            sent += 1


# ---------------------------------------------------------------------------------------------------------------------


MOCK_OPERATIONS = {
    "bibs": mock_sync_bibs,
    "users": mock_sync_users,
    "recipes": mock_sync_recipes,
    "ingredients": mock_sync_ingredients,
    "images": mock_sync_images,
    "orders": mock_sync_orders,
    "loaded_bibs": mock_sync_loaded_bibs,
}

OPERATIONS = {
    "bibs": sync_bibs,
    "users": sync_users,
    "recipes": sync_recipes,
    "ingredients": sync_ingredients,
    "images": sync_images,
    "orders": sync_orders,
    "loaded_bibs": mock_sync_loaded_bibs,
}

DEPENDENCIES = {
    "bibs": [],
    "users": [],
    "recipes": ["bibs", "users"],
    "ingredients": ["bibs", "recipes"],
    "orders": ["recipes", "users"],
    "images": ["recipes"],
    "loaded_bibs": ["bibs"],
}

# ---------------------------------------------------------------------------------------------------------------------


def sync_all(db, operations=OPERATIONS):
    """Sync all from the distant database to the local db."""
    if os.environ["VERBOSE"] == "true":
        print("[i] === Start of Sync ===")
    done = set()
    # 1. Execute all operations with no dependencies
    for operation, dependencies in DEPENDENCIES.items():
        if len(dependencies) == 0:
            operations[operation](db)
            done.add(operation)
    # 2. Execute all operations with dependencies
    while len(done) < len(DEPENDENCIES):
        for operation, dependencies in [
            item for item in DEPENDENCIES.items() if item[0] not in done
        ]:
            try:
                for dependency in dependencies:
                    if dependency not in done:
                        raise SyncDependencyException(
                            f"{operation} depends on {dependency}"
                        )
            except SyncDependencyException:
                continue
            finally:
                operations[operation](db)
                done.add(operation)
    if os.environ["VERBOSE"] == "true":
        print("[i] === End of Sync ===")


def mock_sync_all(db):
    """Mock sync all from the distant database to the local db."""
    sync_all(db, operations=MOCK_OPERATIONS)
