from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from . import Base


class Player(Base):
    __tablename__ = 'player'
    name = Column(String)
    team_id = Column(Integer, ForeignKey('team.id'))
    octane_id = Column(String,unique=True)
    ballchasing_id = Column(String)
    active = Column(Boolean, default=False)


class Team(Base):
    __tablename__ = 'team'
    octane_id = Column(String,unique=True)
    name = Column(String)
    region = Column(String)
    image = Column(String)
    

class Games(Base):
    __tablename__ = 'games'
    date = Column(DateTime)
    title = Column(String)
    team_1 = Column(Integer,ForeignKey('team.id')) ## should be team_id fk 
    team_2 = Column(Integer, ForeignKey('team.id')) ## should be team_id fk, different from team_1 
    is_professional = Column(Boolean)
    game_in_series = Column(Integer)
    duration = Column(Integer)
    octane_id = Column(String,unique=True)

class ScoreboardStats(Base):
    __tablename__ = 'player_stats'
    player_id = Column(Integer,ForeignKey('player.id'))
    game_id = Column(Integer, ForeignKey('games.id'))
    goals = Column(Integer)
    shots = Column(Integer)
    assists = Column(Integer)
    demolitions = Column(Integer)
    saves = Column(Integer)
    score = Column(Integer)

    UniqueConstraint('player_stats.game_id','player_stats.player_id')

    def player_in_table(self,id):
        Player.where(Player.id == id)
