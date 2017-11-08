from datetime import datetime, timedelta
import dateutil

import click
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import func, desc, and_

from tower.database import Session
from tower.model import Post, Following
from tower.helpers import add_tumblr_com


@click.command('top-following')
@click.argument('user-name')
@click.argument('blog-name')
@click.option('--top', default=100)
@click.option('--since-date', default=(datetime.today()-timedelta(days=365)).strftime('%Y-%m-%d'))
def reblogs_per_source(user_name: str, blog_name: str, top: int, since_date: str):
    since_date = dateutil.parser.parse(since_date)

    session = Session()

    df = pd.read_sql(
        session.query(Following.blog_name, func.count(Post.id).label('posts'))
        .filter(
            Following.user_name == user_name
        )
        .outerjoin(Post, and_(
            (Following.blog_name == Post.reblogged_from_name) | (Following.blog_name == Post.reblogged_root_name),
            Post.date >= since_date, Post.blog_name == blog_name)
        )
        .group_by(Following.blog_name).order_by(desc('posts')).limit(top).statement,
        session.bind
    )

    print('Number of posts on {} reblogged from blogs [since {}] followed by {}. This is top {}'.format(
       add_tumblr_com(blog_name), since_date.strftime('%Y-%m-%d'), user_name, top
    ))
    with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
        print(df[['blog_name', 'posts']])

    ax = df[['blog_name', 'posts']][df.posts > 0].plot(
        kind='pie', x='blog_name', y='posts', labels=df.blog_name[df.posts > 0]
    )
    ax.set_xlabel('')
    ax.set_ylabel('')
    plt.show()
