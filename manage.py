import sys
from db.database import SessionLocal, engine
from db import models
from db.crud import delete_user, delete_bib, delete_recipe, delete_ingredient, delete_image, delete_order


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def reset_db():
    db = get_db()
    users = db.query(models.User).all()


commands = {
    'db': {
        'reset': reset_db
    }
}
help = """
    Usage: manage.py <command> [<args>]
    Commands:
"""
for command in commands:
    help += "        {}\n".format(command)
    for subcommand in commands[command]:
        help += "            {}\n".format(subcommand)
help += """    Examples:
        python manage.py db reset
"""

if __name__ == '__main__':
    try:
        command = sys.argv[1]
        if command in commands:
            subcommand = sys.argv[2]
            if subcommand in commands[command]:
                commands[command][subcommand]()
            else:
                print(f'Unknown subcommand \'{subcommand}\'')
                print(help)
        else:
            print(f'Unknown command \'{command}\'')
            print(help)
    except IndexError:
        print(help)
