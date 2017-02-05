#!venv/bin/python

import datetime

from app import db
from app.models import User, Post


def delete_posts():
    for p in Post.query.all():
        db.session.delete(p)
    db.session.commit()


def fix_mail(username):
    user = User.query.filter_by(nickname=username).first()
    if not user.email:
        user.email = '{}@anexample.com'.format(username)
        db.session.commit()


def fix_following(username):
    user = User.query.filter_by(nickname=username).first()
    if user:
        user.follow(user)


def get_user(username):
    user = User.query.filter_by(nickname=username).first()
    if not user:
        new_user = User(nickname=username, email='{}@anexample.com'.format(username.lower()))
        db.session.add(new_user)
        new_user.follow(new_user)
        db.session.commit()
        user = new_user
    fix_mail(username)
    return user


def add_posts(user_posts):
    print('Adding posts for user: ', user_posts['user'])
    user = get_user(user_posts['user'])
    for post in user_posts['posts']:
        new_post = Post(body=post,
                        author=user,
                        timestamp=datetime.datetime.utcnow())
        db.session.add(new_post)
    db.session.commit()


if __name__ == '__main__':
    # Define some posts per user
    carlos_posts = {
        'user': 'Carlos',
        'posts': [
            'I love me!',
            'Working f** had!',
            'This is all nonsense!'
        ]
    }

    juan_posts = {
        'user': 'Juan',
        'posts': [
            'F*******!!',
            'The world is over....',
            'TGIF :D!!',
            'Null',
            'I\'m Don Juan!'
        ]
    }

    susan_posts = {
        'user': 'Susan',
        'posts': [
            'Going on holidays soon!',
            'Just came home...',
            'So tired of everything!'
        ]
    }

    alessandor_posts = {
        'user': 'Alessandro',
        'posts': [
            'I give up politics :(',
            'I can\'t trust people anymore!',
            'I am so depressed!'
        ]
    }

    all_posts = [
        alessandor_posts,
        juan_posts,
        susan_posts,
        carlos_posts
    ]

    delete_posts()

    # Add posts to the database
    for p in all_posts:
        add_posts(p)
        p['user'] = p['user'].lower()
        add_posts(p)

    # Fix users not following themselves
    usernames = ['Alessandro', 'Carlos', 'Juan', 'Susan']

    #for username in usernames:
    #    fix_following(username)
    #    fix_following(username.lower())
    #db.session.commit()
