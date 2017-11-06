import click
import pandas as pd
import matplotlib.pyplot as plt
import dateutil
from datetime import datetime, timedelta

from tower.database import Session
from tower.model import Post


@click.command('top-sources')
@click.argument('blog-name')
@click.option('--top', default=10)
@click.option('--since-date', default=(datetime.today()-timedelta(days=365)).strftime('%Y-%m-%d'))
def top_sources(blog_name: str, top: int, since_date: str):
    since_date = dateutil.parser.parse(since_date)

    session = Session()

    df1 = pd.read_sql(
        session.query(Post).filter(
            Post.date >= since_date,
            Post.blog_name == blog_name,
            Post.reblogged_from_name == Post.reblogged_root_name
        ).statement,
        session.bind
    )
    df2 = pd.read_sql(
        session.query(Post).filter(
            Post.date >= since_date,
            Post.blog_name == blog_name,
            Post.reblogged_from_name != Post.reblogged_root_name
        ).statement,
        session.bind
    )
    df = pd.concat([
        df1['reblogged_from_name'][df1['reblogged_from_name'] != ''],
        df2['reblogged_from_name'][df2['reblogged_from_name'] != ''],
        df2['reblogged_root_name'][df2['reblogged_root_name'] != '']
    ])

    print('Top {} blogs for {} since {}'.format(
        top, blog_name, since_date.strftime('%Y-%m-%d')
    ))
    print(df.value_counts().nlargest(top))

    df.value_counts().plot(kind='pie')
    plt.show()
