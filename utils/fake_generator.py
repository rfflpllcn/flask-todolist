from os.path import join
import random
from datetime import datetime

import forgery_py

from app import db
from app.models import Idea, Portfolio, User, Instrument

# from config import BASEDIR
# DATA_ROOT = join(BASEDIR, 'data')
from data.instruments import INSTRUMENTS


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
        instruments = Instrument.query.all()

        assert portfolios != []
        assert instruments != []

        for _ in range(count):
            portfolio = random.choice(portfolios)
            instrument = random.choice(instruments)
            idea = Idea(
                description=forgery_py.forgery.lorem_ipsum.words(),
                portfolio_id=portfolio.id,
                instrument_id=instrument.id,
                creator=portfolio.creator,
                created_at=self.generate_fake_date(),
            ).save()
            if random.choice([True, False]):
                idea.finished()

    def generate_fake_instruments(self):
        
        for instrument in INSTRUMENTS:
            isin = instrument['isin']
            short_name = instrument['shortName']
            name = instrument['name']
            sustainable = instrument['sustainable']
            responsible = instrument['responsible']
            sakmCioSas3Name = instrument['sakmCioSas3Name']
            sakmCioCurrencyCode = instrument['sakmCioCurrencyCode']
            sakmCioCountryCode = instrument['sakmCioCountryCode']

            esg = ''
            if 'sustainabilityFactors' in instrument:
                d = instrument['sustainabilityFactors']
                for di in d:
                    if (di['sustainabilityType'] == 'ESG') and (di['factorType'] == 'ESG_RATING'):
                        esg = di['factorValue']

            Instrument(
                isin=isin,
                short_name=short_name,
                name=name,
                sustainable=sustainable,
                responsible=responsible,
                sakmCioSas3Name=sakmCioSas3Name,
                sakmCioCurrencyCode=sakmCioCurrencyCode,
                sakmCioCountryCode=sakmCioCountryCode,
                esg=esg
            ).save()

    def generate_fake_data(self, count):
        # generation must follow this order, as each builds on the previous
        self.generate_fake_users(count)
        self.generate_fake_portfolios(count * 4)
        self.generate_fake_instruments()
        self.generate_fake_idea(count * 16)

    def start(self, count=10):
        self.generate_fake_data(count)
