from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.schemas import BibCreate, UserCreate, RecipeCreate, IngredientCreate, ImageCreate
from utils import diff, as_dict
from base64 import b64encode
import os


class SyncDependencyException(Exception):
    """ Used for dependency sync dependency calculations """
    pass

# ---------------------------------------------------------------------------------------------------------------------


def mock_sync_bibs(db):
    """Sync bibs from the distant database to the local db."""
    local_bibs = list(map(as_dict, crud.get_bibs(db)))
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
    delete_count = 0
    for local_bib in local_bibs:
        if local_bib['id'] not in [bib['id'] for bib in mock_distant_bibs]:
            crud.delete_bib(db, local_bib['id'])
            delete_count += 1
    add_count = 0
    for local_bib in mock_distant_bibs:
        if local_bib['id'] not in [bib['id'] for bib in local_bibs]:
            crud.create_bib(db, BibCreate(**local_bib))
            add_count += 1
    if os.environ['VERBOSE'] == 'true': print(f'deleted {delete_count} bib(s), added {add_count} bib(s)')


def mock_sync_users(db):
    """Sync users from the distant database to the local db."""
    local_users = list(map(as_dict, crud.get_users(db)))
    mock_distant_users = [
        {'id': 1, 'name': 'Cocktail.me', 'role': 'admin'}
    ]
    delete_count = 0
    for local_user in local_users:
        if local_user['id'] not in [user['id'] for user in mock_distant_users]:
            crud.delete_user(db, local_user['id'])
            delete_count += 1
    add_count = 0
    for local_user in mock_distant_users:
        if local_user['id'] not in [user['id'] for user in local_users]:
            crud.create_user(db, UserCreate(**local_user))
            add_count += 1
    if os.environ['VERBOSE'] == 'true': print(f'deleted {delete_count} user(s), added {add_count} user(s)')


def mock_sync_recipes(db):
    """Sync recipes from the distant database to the local db."""
    local_recipes = list(map(as_dict, crud.get_recipes(db)))
    mock_distant_recipes = [
        {'id': 1, 'title': 'Mojito', 'description': 'mojito', 'author_id': 1},
        {'id': 2, 'title': 'Punch', 'description': 'punch', 'author_id': 1},
        {'id': 3, 'title': 'Piña colada', 'description': 'piña colada', 'author_id': 1},
        {'id': 4, 'title': 'Margarita', 'description': 'margarita', 'author_id': 1},
        {'id': 5, 'title': 'Cosmopolitan', 'description': 'cosmopolitan', 'author_id': 1},
        {'id': 6, 'title': 'Blue Lagoon', 'description': 'blue lagoon', 'author_id': 1},
        {'id': 7, 'title': 'Sex on the beach', 'description': 'sex on the beach', 'author_id': 1},
    ]
    delete_count = 0
    for local_recipe in local_recipes:
        if local_recipe['id'] not in [recipe['id'] for recipe in mock_distant_recipes]:
            crud.delete_recipe(db, local_recipe['id'])
            delete_count += 1
    add_count = 0
    for recipe in mock_distant_recipes:
        if recipe['id'] not in [local_recipe['id'] for local_recipe in local_recipes]:
            crud.create_recipe(db, RecipeCreate(**recipe))
            add_count += 1
    if os.environ['VERBOSE'] == 'true': print(f'deleted {delete_count} recipe(s), added {add_count} recipe(s)')


def mock_sync_ingredients(db):
    """Sync ingredients from the distant database to the local db."""
    local_ingredients = list(map(as_dict, crud.get_ingredients(db)))
    mock_distant_ingredients = [
        {'recipe_id': 1, 'bib_id': 1, 'amount': 60},
        {'recipe_id': 1, 'bib_id': 14, 'amount': 200},
        {'recipe_id': 1, 'bib_id': 8, 'amount': 30},
        {'recipe_id': 1, 'bib_id': 12, 'amount': 20},
        {'recipe_id': 2, 'bib_id': 1, 'amount': 100},
        {'recipe_id': 2, 'bib_id': 12, 'amount': 50},
        {'recipe_id': 2, 'bib_id': 15, 'amount': 100},
        {'recipe_id': 2, 'bib_id': 16, 'amount': 100},
        {'recipe_id': 3, 'bib_id': 1, 'amount': 40},
        {'recipe_id': 3, 'bib_id': 2, 'amount': 20},
        {'recipe_id': 3, 'bib_id': 16, 'amount': 120},
        {'recipe_id': 3, 'bib_id': 17, 'amount': 40},
        {'recipe_id': 4, 'bib_id': 3, 'amount': 50},
        {'recipe_id': 4, 'bib_id': 4, 'amount': 30},
        {'recipe_id': 4, 'bib_id': 8, 'amount': 20},
        {'recipe_id': 5, 'bib_id': 5, 'amount': 40},
        {'recipe_id': 5, 'bib_id': 4, 'amount': 20},
        {'recipe_id': 5, 'bib_id': 9, 'amount': 20},
        {'recipe_id': 5, 'bib_id': 8, 'amount': 10},
        {'recipe_id': 6, 'bib_id': 5, 'amount': 40},
        {'recipe_id': 6, 'bib_id': 10, 'amount': 30},
        {'recipe_id': 6, 'bib_id': 7, 'amount': 20},
        {'recipe_id': 7, 'bib_id': 5, 'amount': 30},
        {'recipe_id': 7, 'bib_id': 16, 'amount': 50},
        {'recipe_id': 7, 'bib_id': 9, 'amount': 60},
        {'recipe_id': 7, 'bib_id': 18, 'amount': 10},
    ]
    delete_count = 0
    for local_ingredient in local_ingredients:
        if (local_ingredient['recipe_id'],local_ingredient['bib_id']) not in [(ingredient['recipe_id'],ingredient['bib_id']) for ingredient in mock_distant_ingredients]:
            crud.delete_ingredient(db, local_ingredient['id'])
            delete_count += 1
    add_count = 0
    for ingredient in mock_distant_ingredients:
        if (ingredient['recipe_id'],ingredient['bib_id']) not in [(local_ingredient['recipe_id'],local_ingredient['bib_id']) for local_ingredient in local_ingredients]:
            crud.create_ingredient(db, IngredientCreate(**ingredient))
            add_count += 1
    if os.environ['VERBOSE'] == 'true': print(f'deleted {delete_count} ingredient(s), added {add_count} ingredient(s)')


def mock_sync_images(db):
    """Sync images from the distant database to the local db."""
    local_images = list(map(as_dict,crud.get_images(db)))
    mock_distant_images = []
    for filename in os.listdir('mock/images'):
        with open(filename, 'rb') as file:
            mock_distant_images.append({'id': filename.split('.')[0], 'data': b64encode(file.read())})
    delete_count = 0
    for local_image in local_images:
        if local_image['id'] not in [image['id'] for image in mock_distant_images]:
            crud.delete_image(db, local_image['id'])
            delete_count += 1
    add_count = 0
    for image in mock_distant_images:
        if image['id'] not in [local_image['id'] for local_image in local_images]:
            crud.create_image(db, ImageCreate(**image))
            add_count += 1
    if os.environ['VERBOSE'] == 'true': print(f'deleted {delete_count} image(s), added {add_count} image(s)')


def mock_sync_orders(db):
    """Sync orders from the local database to the distant db."""
    local_orders = list(map(as_dict, crud.get_orders(db)))
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
    for operation, dependencies in DEPENDENCIES.items():
        if len(dependencies) == 0:
            operations[operation](db)
            done.add(operation)
    # 2. Execute all operations with dependencies
    while len(done) < len(DEPENDENCIES):
        for operation, dependencies in [item for item in DEPENDENCIES.items() if item[0] not in done]:
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
