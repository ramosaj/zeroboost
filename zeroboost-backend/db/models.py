from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from . import Base


class Player(Base):
    __tablename__ = 'player'
    name = Column(String)
    team_id = Column(Integer)
    octane_id = Column(String)
    ballchasing_id = Column(String)


class Team(Base):
    __tablename__ = 'team'
    octane_id = Column(String)
    name = Column(String)
    region = Column(String)
    image = Column(String)
    

class Games(Base):
    __tablename__ = 'games'
    date = Column(Date)
    title = Column(String)
    team_1 = Column(Integer) ## should be team_id fk 
    team_2 = Column(Integer) ## should be team_id fk, different from team_1 
    is_professional = Column(Boolean)


class ScoreboardStats(Base):
    __tablename__ = 'player_stats'
    player_id = Column(Integer)
    game_id = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    demolitions = Column(Integer)
    score = Column(Integer)