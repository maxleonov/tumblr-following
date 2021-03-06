### Idea
Build a helper tool that helps a Tumblr user to clean up the list of blogs they follow.

### User story
As a Tumblr user myself, I found that:
- I follow hundreds of blogs, or even more
- I _know_ that many of these blogs are probably dead (no posts in the last months/years)
- I _know_ that many of these blogs produce _many_ posts that I'm _not_ interested in and very _few_ that I am
- I _assume_ that by cleaning up the list of blogs I follow:
    - My timeline will become shorter and more relevant
    - I will spend less time digging through the garbage and more time enjoying the content I'm interested in
    - I will spend less time on Tumblr in general
- As the result, I want to follow as few blogs as possible
- To achieve this, I want to be able to unfollow the blogs that I choose based on the numbers
- Additionally, I'm just curious in seeing some general analytics:
    - list of blogs I mostly reblog from

### (First) goals
Display the following data to a Tumblr user:
- blogs they reblog from the most
- blogs they might want to unfollow (dead or not reblogged from)

### Technology stack:
- Python 3.6+
    - SQLAlchemy
    - Click
    - PyTumblr
    - Pandas
- SQLite

### Installation
Install [Pyenv](https://github.com/pyenv/pyenv#installation)
```
git clone https://github.com/maxleonov/tumblr-following.git
cd tumblr-following
PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install --skip-existing 3.6.1
pyenv local 3.6.1
python3.6 -m venv venv
. venv/bin/activate
pip install -e .
```

### Running
```
$ tower
Usage: tower [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  fetch-following
  fetch-posts
  suggest-unfollowing
  top-following
  top-sources
```
