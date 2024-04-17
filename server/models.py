from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # add relationship
    hero_powers = db.Relationship('HeroPower', back_populates= 'hero', cascade="all, delete-orphan")

    # add serialization rules
    serialize_rules = ('-hero_powers.hero',)


    def __repr__(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # add relationship
    hero_powers = db.Relationship('HeroPower', back_populates= 'power',  cascade="all, delete-orphan")


    # add serialization rules
    serialize_rules = ('-hero_powers.power',)

    # add validation
    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be atleast 20 characters long")
        return description 

    def __repr__(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # add relationships
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable = False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable = False)

    hero = db.Relationship('Hero', back_populates= 'hero_powers')
    power = db.Relationship('Power', back_populates= 'hero_powers')



    # add serialization rules
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers',)

    # add validation
    @validates('strength')
    def validates_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be Strong, Weak, or Average")
        return strength


    def __repr__(self):
        return f'<HeroPower {self.id}>'
