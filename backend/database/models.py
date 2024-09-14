from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, JSON, Boolean
from sqlalchemy.orm import relationship
from backend.database.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_confirmed = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, nullable=False)

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey('users.id'))
    player2_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP, nullable=False)

    player1 = relationship("User", foreign_keys=[player1_id])
    player2 = relationship("User", foreign_keys=[player2_id])

    # Add this line to define the relationship with rounds
    rounds = relationship("Round", back_populates="game")

class Round(Base):
    __tablename__ = "rounds"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    player1_input = Column(JSON, nullable=True)
    player2_input = Column(JSON, nullable=True)
    letter = Column(String(1), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    game = relationship("Game", back_populates="rounds")
    scores = relationship("Score", back_populates="round")

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    round_id = Column(Integer, ForeignKey('rounds.id'))
    player1_score = Column(Integer, nullable=False, default=0)
    player2_score = Column(Integer, nullable=False, default=0)

    round = relationship("Round", back_populates="scores")

class Opponent(Base):
    __tablename__ = "opponents"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey('users.id'))
    opponent_id = Column(Integer, ForeignKey('users.id'))
    game_id = Column(Integer, ForeignKey('games.id'))
    last_played = Column(TIMESTAMP, nullable=False)

    player = relationship("User", foreign_keys=[player_id])
    opponent = relationship("User", foreign_keys=[opponent_id])