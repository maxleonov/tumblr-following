##### Idea
Build a helper tool that helps a Tumblr user to clean up the list of blogs they follow.

#### User story
As a Tumblr user myself, I found that:
- I follow `'\d{3,}'` blogs
- I _know_ that many of these blogs are probably dead (no posts in the last months/years)
- I _know_ that many of these blogs produce _many_ posts that I'm _not_ interested and very few that I am
- I _suspect_ that by cleaning up the list of blogs I follow:
    - My timeline will become shorter and more relevant
    - I will spend less time digging through the garbage and more time enjoying the content I'm interested in
    - I will spend less time on Tumblr in general
- Additionally, I'm just curious in seeing some general analytics:
    - list of blogs I mostly reblog from
    - how many posts do I have per period (yearly, monthly, daily, in total)
- As the result, I want to follow as few blogs as possible
- Which is, I want to be able to unfollow the blogs that I choose based on the numbers

#### (First) goals
Display the following data to a Tumblr user:
- blogs they reblog from the most
- blogs they might want to unfollow (dead or not reblogged from)

#### Technology stack:
- Python 3.6+
    - SQLAlchemy
    - Click
    - PyTumblr
    - Pandas
- SQLite
