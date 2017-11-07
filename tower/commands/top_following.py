from datetime import datetime, timedelta

import click
import pandas as pd
import matplotlib.pyplot as plt
import dateutil
from sqlalchemy import func, desc

from tower.database import Session
from tower.model import Post, Following


@click.command('top-following')
@click.argument('blog-name')
@click.option('--top', default=10)
@click.option('--since-date', default=(datetime.today()-timedelta(days=365)).strftime('%Y-%m-%d'))
def reblogs_per_source(blog_name: str, top: int, since_date: str):
    since_date = dateutil.parser.parse(since_date)

    session = Session()

    df = pd.read_sql(
        session.query(Following.name, func.count(Post.id).label('count')).filter(
            Post.date >= since_date,
            Post.blog_name == blog_name,
            (Following.name == Post.reblogged_from_name) | (Following.name == Post.reblogged_root_name)
        ).group_by(Following.name).order_by(desc('count')).limit(top).statement,
        session.bind
    )

    # print('Following distribution: Top {} blogs followed by {} since {}'.format(
    #    top, blog_name, since_date.strftime('%Y-%m-%d')
    # ))
    print(df[['name', 'count']])

    df[['name', 'count']].plot(kind='pie', x='name', y='count', labels=df['name'])
    plt.show()
