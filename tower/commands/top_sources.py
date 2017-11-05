import click
import pandas as pd
import matplotlib.pyplot as plt

from tower.database import engine
from tower.model import Post


@click.command('top-sources')
@click.option('--top', default=10)
def top_sources(top: int):
    df = pd.read_sql_table(
        table_name=Post.__tablename__,
        con=engine,
        columns=['reblogged_from_name', 'reblogged_root_name']
    )
    print(df['reblogged_from_name'][df['reblogged_from_name'] != ''].value_counts().nlargest(top))
    print(df['reblogged_root_name'][df['reblogged_root_name'] != ''].value_counts().nlargest(top))
    # df['reblogged_from_name'][df['reblogged_from_name'] != ''].value_counts().plot(kind='pie')
    # plt.show()
