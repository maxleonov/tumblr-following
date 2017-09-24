import click

from tower.commands.fetch_posts import fetch_posts
from tower.database import engine
from tower.logging import setup_logging
from tower.model import Base


@click.group()
def main():
	setup_logging()
	Base.metadata.create_all(engine)


main.add_command(fetch_posts)


if __name__ == '__main__':
	main()
