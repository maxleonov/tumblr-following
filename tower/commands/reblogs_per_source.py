from datetime import datetime, timedelta

import click
import pandas as pd
import matplotlib.pyplot as plt
import dateutil
from sqlalchemy import func

from tower.database import Session
from tower.model import Post, Following


@click.command('reblogs-per-source')
@click.argument('blog-name')
@click.option('--top', default=10)
@click.option('--since-date', default=(datetime.today()-timedelta(days=365)).strftime('%Y-%m-%d'))
def reblogs_per_source(blog_name: str, top: int, since_date: str):
    since_date = dateutil.parser.parse(since_date)

    session = Session()

    df = pd.read_sql(
        session.query(Following.name, func.count(Post.id)).filter(
            Post.date >= since_date,
            Post.blog_name == blog_name,
            (Following.name == Post.reblogged_from_name) | (Following.name == Post.reblogged_root_name)
        ).group_by(Following.name).order_by('count_1 DESC').statement,
        session.bind
    )

    print(df[['name', 'count_1']])

    df[['name', 'count_1']].plot(kind='pie', x='name', y='count_1', labels=df['name'])
    plt.show()
