from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.schemas import BibCreate, UserCreate, RecipeCreate, IngredientCreate, ImageCreate
from utils import diff
from base64 import b64encode
import os


class SyncDependencyException(Exception):
    """ Used for dependency sync dependency calculations """
    pass

# ---------------------------------------------------------------------------------------------------------------------


def mock_sync_bibs(db):
    """Sync bibs from the distant database to the local db."""
    local_bibs = crud.get_bibs(db)
    mock_distant_bibs = [
        {'id': 1, 'name': "rhum blanc"},
        {'id': 2, 'name': "rhum ambré"},
        {'id': 3, 'name': "tequila"},
        {'id': 4, 'name': "grand marnier"},
        {'id': 5, 'name': "vodka"},
        {'id': 6, 'name': "cognac"},
        {'id': 7, 'name': "jus de citron"},
        {'id': 8, 'name': "jus de citron vert"},
        {'id': 9, 'name': "jus de cranberry"},
        {'id': 10, 'name': "curaçao bleu"},
        {'id': 11, 'name': "sirop de menthe"},
        {'id': 12, 'name': "sirop de sucre de canne"},
        {'id': 13, 'name': "sirop de melon"},
        {'id': 14, 'name': "eau gazeuse"},
        {'id': 15, 'name': "jus d'orange"},
        {'id': 16, 'name': "jus d'ananas"},
        {'id': 17, 'name': "lait de coco"},
        {'id': 18, 'name': "crème de pêche"}
    ]
    difference = diff(local_bibs, mock_distant_bibs)
    if os.environ['VERBOSE'] == 'true': print(f'downloaded {len(difference)} new bib(s)')

    for bib in difference:
        crud.create_bib(db, BibCreate(**bib))


def mock_sync_users(db):
    """Sync users from the distant database to the local db."""
    local_users = crud.get_users(db)
    mock_distant_users = [
        {'id': 1, 'name': 'Cocktail.me'}
    ]
    difference = diff(local_users, mock_distant_users)
    if os.environ['VERBOSE'] == 'true': print(f'downloaded {len(difference)} new user(s)')
    for user in difference:
        crud.create_user(db, UserCreate(**user))
    pass


def mock_sync_recipes(db):
    """Sync recipes from the distant database to the local db."""
    local_recipes = crud.get_recipes(db)
    mock_distant_recipes = [
        {'id': 1, 'title': 'Mojito', 'description': 'mojito', 'image_id': 1, 'author_id': 1},
        {'id': 2, 'title': 'Punch', 'description': 'punch', 'image_id': 2, 'author_id': 1},
        {'id': 3, 'title': 'Piña colada', 'description': 'piña colada', 'image_id': 3, 'author_id': 1},
        {'id': 4, 'title': 'Margarita', 'description': 'margarita', 'image_id': 4, 'author_id': 1},
        {'id': 5, 'title': 'Cosmopolitan', 'description': 'cosmopolitan', 'image_id': 5, 'author_id': 1},
        {'id': 6, 'title': 'Blue Lagoon', 'description': 'blue lagoon', 'image_id': 6, 'author_id': 1},
        {'id': 7, 'title': 'Sex on the beach', 'description': 'sex on the beach', 'image_id': 7, 'author_id': 1},
    ]
    difference = diff(local_recipes, mock_distant_recipes)
    if os.environ['VERBOSE'] == 'true': print(f'downloaded {len(difference)} new user(s)')
    for recipe in difference:
        crud.create_recipe(db, RecipeCreate(**recipe))
    pass


def mock_sync_ingredients(db):
    """Sync ingredients from the distant database to the local db."""
    local_ingredients = crud.get_ingredients(db)
    mock_distant_ingredients = [
        {'recipe_id': 1, 'bib_id': 1, 'quantity': 60},
        {'recipe_id': 1, 'bib_id': 14, 'quantity': 200},
        {'recipe_id': 1, 'bib_id': 8, 'quantity': 30},
        {'recipe_id': 1, 'bib_id': 12, 'quantity': 20},
        {'recipe_id': 2, 'bib_id': 1, 'quantity': 100},
        {'recipe_id': 2, 'bib_id': 12, 'quantity': 50},
        {'recipe_id': 2, 'bib_id': 15, 'quantity': 100},
        {'recipe_id': 2, 'bib_id': 16, 'quantity': 100},
        {'recipe_id': 3, 'bib_id': 1, 'quantity': 40},
        {'recipe_id': 3, 'bib_id': 2, 'quantity': 20},
        {'recipe_id': 3, 'bib_id': 16, 'quantity': 120},
        {'recipe_id': 3, 'bib_id': 17, 'quantity': 40},
        {'recipe_id': 4, 'bib_id': 3, 'quantity': 50},
        {'recipe_id': 4, 'bib_id': 4, 'quantity': 30},
        {'recipe_id': 4, 'bib_id': 8, 'quantity': 20},
        {'recipe_id': 5, 'bib_id': 5, 'quantity': 40},
        {'recipe_id': 5, 'bib_id': 4, 'quantity': 20},
        {'recipe_id': 5, 'bib_id': 9, 'quantity': 20},
        {'recipe_id': 5, 'bib_id': 8, 'quantity': 10},
        {'recipe_id': 6, 'bib_id': 5, 'quantity': 40},
        {'recipe_id': 6, 'bib_id': 10, 'quantity': 30},
        {'recipe_id': 6, 'bib_id': 7, 'quantity': 20},
        {'recipe_id': 7, 'bib_id': 5, 'quantity': 30},
        {'recipe_id': 7, 'bib_id': 16, 'quantity': 50},
        {'recipe_id': 7, 'bib_id': 9, 'quantity': 60},
        {'recipe_id': 7, 'bib_id': 18, 'quantity': 10},
    ]
    difference = diff(local_ingredients, mock_distant_ingredients)
    if os.environ['VERBOSE'] == 'true': print(f'downloaded {len(difference)} new user(s)')
    for ingredient in difference:
        crud.create_ingredient(db, IngredientCreate(**ingredient))
    pass


def mock_sync_images(db):
    """Sync images from the distant database to the local db."""
    local_images = crud.get_images(db)
    mock_distant_images = []
    for filename in os.listdir('mock/images'):
        with open(filename, 'rb') as file:
            mock_distant_images.append({'id': filename.split('.')[0], 'data': b64encode(file.read())})
    difference = diff(local_images, mock_distant_images)
    if os.environ['VERBOSE'] == 'true': print(f'downloaded {len(difference)} new user(s)')
    for image in difference:
        crud.create_image(db, ImageCreate(**image))


def mock_sync_orders(db):
    """Sync orders from the local database to the distant db."""
    local_orders = crud.get_orders(db)
    mock_distant_orders = []
    if os.environ['VERBOSE'] == 'true': print(f'sent {len(local_orders)} new order(s)')
    for order in local_orders:
        mock_distant_orders.append(order)
        crud.delete_order(db, order['id'])


# ---------------------------------------------------------------------------------------------------------------------


def sync_bibs(db):
    """Sync bibs from the distant database to the local db."""
    pass


def sync_users(db):
    """Sync users from the distant database to the local db."""
    pass


def sync_recipes(db):
    """Sync recipes from the distant database to the local db."""
    pass


def sync_ingredients(db):
    """Sync ingredients from the distant database to the local db."""
    pass


def sync_images(db):
    """Sync images from the distant database to the local db."""
    pass


def sync_orders(db):
    """Sync orders from the local database to the distant db."""
    pass

# ---------------------------------------------------------------------------------------------------------------------


MOCK_OPERATIONS = {
    'bibs': mock_sync_bibs,
    'users': mock_sync_users,
    'recipes': mock_sync_recipes,
    'ingredients': mock_sync_ingredients,
    'images': mock_sync_images,
    'orders': mock_sync_orders
}

OPERATIONS = {
    'bibs': sync_bibs,
    'users': sync_users,
    'recipes': sync_recipes,
    'ingredients': sync_ingredients,
    'images': sync_images,
    'orders': sync_orders
}

DEPENDENCIES = {
    'bibs': [],
    'users': [],
    'recipes': ['bibs', 'users'],
    'ingredients': ['bibs', 'recipes'],
    'orders': ['recipes', 'users'],
}

# ---------------------------------------------------------------------------------------------------------------------


def sync_all(db, operations=OPERATIONS):
    """Sync all from the distant database to the local db."""
    if os.environ['VERBOSE'] == 'true': print('[i] === Start of Sync ===')
    done = set()
    # 1. Execute all operations with no dependencies
    for operation, dependencies in DEPENDENCIES:
        if len(dependencies) == 0:
            operations[operation](db)
            done.add(operation)
    # 2. Execute all operations with dependencies
    while len(done) < len(DEPENDENCIES):
        for operation, dependencies in {item for item in DEPENDENCIES.items() if item[0] not in done}:
            try:
                for dependency in dependencies:
                    if dependency not in done:
                        raise SyncDependencyException(f'{operation} depends on {dependency}')
            except SyncDependencyException:
                continue
            finally:
                operations[operation](db)
                done.add(operation)
    if os.environ['VERBOSE'] == 'true': print('[i] === End of Sync ===')


def mock_sync_all(db):
    """Mock sync all from the distant database to the local db."""
    sync_all(db, operations=MOCK_OPERATIONS)
