from datetime import datetime, timedelta
import dateutil

import click
import pandas as pd
from sqlalchemy import func, desc, and_

from tower.database import Session
from tower.model import Post, Following
from tower.helpers import add_tumblr_com


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

    print(
        'Use this information at your own risk.\n'
        'It\'s up to the user to decide if this approach aligns with the way they use their Tumblr account.\n\n'
        'Please make sure to read and understand the workflow:\n'
        '1. Calculate statistics:\n'
        'We checks the list of blogs followed by {} ...\n'
        'and calculate the number of posts reblogged from each blog to {} since {}.\n'
        '2. Provide suggestions:\n'
        'If the number of reblogs is less than {}, we suggest considering to unfollow the blog.\n\n'
        'The commands below can be used to unfollow blogs, as explained above:\n\n'
        'python tower/interactive_console.py\n'
        'blogs = {}\n'
        'for blog in blogs:\n'
        '    client.unfollow(blog)'
        .format(
            user_name, add_tumblr_com(blog_name), since_date.strftime('%Y-%m-%d'), reblogs_less_than,
            [blog for blog in list(df.blog_name[df.posts < reblogs_less_than])]
        )
    )
