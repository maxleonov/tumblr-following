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
    value_counts = pd.concat([
        df1['reblogged_from_name'][df1['reblogged_from_name'] != ''],
        df2['reblogged_from_name'][df2['reblogged_from_name'] != ''],
        df2['reblogged_root_name'][df2['reblogged_root_name'] != '']
    ]).value_counts().nlargest(top)

    # Convert to pd.DataFrame. In fact, this step is not necessary and is resource-greedy. Still, I want to treat the piece of data as a DataFrame.
    value_counts = dict(value_counts)
    df = pd.DataFrame({
        'name': list(value_counts.keys()),
        'posts': list(value_counts.values())
    })

    print('Top {} blogs reblogged on {} since {}'.format(
        top, blog_name, since_date.strftime('%Y-%m-%d')
    ))
    with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
        print(df[['name', 'posts']])

    ax = df[['name', 'posts']].plot(kind='pie', x='name', y='posts', labels=df['name'])
    ax.set_xlabel('')
    ax.set_ylabel('')
    plt.show()
