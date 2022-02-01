import random
from datetime import datetime

import forgery_py

from app import db
from app.models import Idea, Portfolio, User


class FakeGenerator:
    def __init__(self):
        # in case the tables haven't been created already
        db.drop_all()
        db.create_all()

    def generate_fake_date(self):
        return datetime.combine(forgery_py.date.date(True), datetime.utcnow().time())

    def generate_fake_users(self, count):
        for _ in range(count):
            User(
                email=forgery_py.internet.email_address(),
                username=forgery_py.internet.user_name(True),
                password="correcthorsebatterystaple",
                member_since=self.generate_fake_date(),
            ).save()

    def generate_fake_portfolios(self, count):
        # for the creator relation we need users
        users = User.query.all()
        assert users != []
        for _ in range(count):
            Portfolio(
                title=forgery_py.forgery.lorem_ipsum.title(),
                creator=random.choice(users).username,
                created_at=self.generate_fake_date(),
            ).save()

    def generate_fake_idea(self, count):
        # for the portfolio relation we need portfolios
        portfolios = Portfolio.query.all()
        assert portfolios != []
        for _ in range(count):
            portfolio = random.choice(portfolios)
            idea = Idea(
                description=forgery_py.forgery.lorem_ipsum.words(),
                portfolio_id=portfolio.id,
                creator=portfolio.creator,
                created_at=self.generate_fake_date(),
            ).save()
            if random.choice([True, False]):
                idea.finished()

    def generate_fake_data(self, count):
        # generation must follow this order, as each builds on the previous
        self.generate_fake_users(count)
        self.generate_fake_portfolios(count * 4)
        self.generate_fake_idea(count * 16)

    def start(self, count=10):
        self.generate_fake_data(count)
