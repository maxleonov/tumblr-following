import click

from tower.commands.fetch_following import fetch_following
from tower.commands.fetch_posts import fetch_posts
from tower.commands.top_sources import top_sources
from tower.commands.reblogs_per_source import reblogs_per_source
from tower.database import engine
from tower.log import setup_logging
from tower.model import Base


@click.group()
def main():
    setup_logging()
    Base.metadata.create_all(engine)


main.add_command(fetch_posts)
main.add_command(fetch_following)
main.add_command(top_sources)
main.add_command(reblogs_per_source)

if __name__ == '__main__':
    main()
