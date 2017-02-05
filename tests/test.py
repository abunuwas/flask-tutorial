#!venv/bin/python
from datetime import datetime, timedelta
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Post


class DBSetUp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestUniqueNicknames(DBSetUp):
    def test_make_unique_nickname(self):
        u = User(nickname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('john')
        self.assertNotEqual(nickname, 'john')


class TestFollowers(DBSetUp):
    def setUp(self):
        DBSetUp.setUp(self)
        self.u1 = User(nickname='john', email='john@example.com')
        self.u2 = User(nickname='susan', email='susan@example.com')
        db.session.add(self.u1)
        db.session.add(self.u2)
        db.session.commit()
        u = self.u1.follow(self.u2)
        db.session.add(u)
        db.session.commit()

    def test_unfollow_not_none(self):
        self.assertIsNotNone(self.u1.unfollow(self.u2))

    def test_follow(self):
        self.assertIsNone(self.u1.follow(self.u2))

    def test_is_following(self):
        self.assertTrue(self.u1.is_following(self.u2))

    def test_followed_count(self):
        self.assertEqual(self.u1.followed.count(), 1)

    def test_followed_identity(self):
        self.assertEqual(self.u1.followed.first().nickname, 'susan')

    def test_follower_count(self):
        self.assertEqual(self.u2.followers.count(), 1)

    def test_follower_identity(self):
        self.assertEqual(self.u2.followers.first().nickname, 'john')

    def test_unfollow_is_none(self):
        u = self.u1.unfollow(self.u2)
        db.session.add(u)
        db.session.commit()
        self.assertIsNone(self.u1.unfollow(self.u2))
        u = self.u1.follow(self.u2)
        db.session.add(u)
        db.session.commit()


class TestFollowedPosts(DBSetUp):
    def setUp(self):
        DBSetUp.setUp(self)
        self.u1 = User(nickname='john', email='j@j.com')
        self.u2 = User(nickname='mary', email='m@m.com')
        self.users = [self.u1, self.u2]
        for user in self.users:
            db.session.add(user)
        db.session.commit()
        utcnow = datetime.utcnow()
        self.p1 = Post(body='post from john',
                       author=self.u1,
                       timestamp=utcnow + timedelta(seconds=1))
        self.p2 = Post(body='post from mary',
                       author=self.u2,
                       timestamp=utcnow + timedelta(seconds=2))
        self.posts = [self.p1, self.p2]
        for post in self.posts:
            db.session.add(post)
        db.session.commit()
        self.u1.follow(self.u1)
        self.u1.follow(self.u2)
        self.u2.follow(self.u2)

    def test_posts_identity(self):
        outcome = self.u1.followed_posts().all()
        expected = [self.p2, self.p1]
        self.assertEqual(outcome, expected)

class TestUtils(unittest.TestCase):
    def test_avatar(self):
        u = User(nickname='john', email='john@example.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        self.assertEqual(avatar[0:len(expected)], expected)


if __name__ == '__main__':
    unittest.main()
