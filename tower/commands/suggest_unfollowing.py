from datetime import datetime, timedelta
import dateutil

import click
import pandas as pd
from sqlalchemy import func, desc, and_

from tower.database import Session
from tower.model import Post, Following


@click.command('suggest-unfollowing')
@click.argument('user-name')
@click.argument('blog-name')
@click.option('--since-date', default=(datetime.today()-timedelta(days=365)).strftime('%Y-%m-%d'))
@click.option('--reblogs-less-than', default=1)
def suggest_unfollowing(user_name: str, blog_name: str, since_date: str, reblogs_less_than=1):
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
        .group_by(Following.blog_name).order_by(desc('posts')).statement,
        session.bind
    )

    print(  # TODO improve wording
        'Some blogs are being followed but have less than {} reblog(s) to {} since {}.\n'
        'The idea here is that a user might want to unfollow blogs that they follow don\'t reblog.\n'
        'Please use at your own risk and make sure you udnerstand what the below code does.\n'
        'Consider unfollowing them:\n'
        'python tower/interactive_console.py\n'
        'blogs = {}\n'
        'for blog in blogs:\n'
        '    client.unfollow(blog)'
        .format(
            reblogs_less_than, blog_name, since_date.strftime('%Y-%m-%d'),
            [blog for blog in list(df.blog_name[df.posts < reblogs_less_than])]
        )
    )
