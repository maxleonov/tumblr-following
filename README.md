### Idea
Build a helper tool that helps a Tumblr user to clean up the list of blogs they follow.

### User story
As a Tumblr user myself, I found that:
- I follow `'\d{3,}'` blogs
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
    - how many posts do I have per period (yearly, monthly, daily, in total)

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

### How to
#### Install the app
Install [Pyenv](https://github.com/pyenv/pyenv#installation)
```
git clone https://github.com/maxleonov/tumblr-following.git
cd tumblr-following
pyenv install --skip-existing 3.6.1
pyenv local 3.6.1
pip install virtualenv
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

#### Set up OAuth credentials
1. Authorize [Tower](https://www.tumblr.com/oauth/authorize?oauth_token=8mr7OT8H2LtOCRESV3ulrL910lDYDnSt3zOmVXjoj5VPo2yVBr) to access account data
2. Click _Python_
3. Copy keys to tower/tumblr_client.py (this is a temporary solution, until a proper way of storing the OAuth credentials is introduced)

#### Run the app
TODO
