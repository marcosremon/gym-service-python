from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from src.transversal.utils.base import Base

class UserFriend(Base):
    __tablename__ = 'user_friends'
    
    user_friend_id: int = Column(BigInteger, primary_key=True, autoincrement=True)
    
    user_id: int = Column(
        BigInteger, 
        ForeignKey('users.user_id', ondelete='CASCADE'),
        nullable=False
    )
    
    friend_id: int = Column(
        BigInteger,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        nullable=False
    )
    
    user = relationship(
        "User", 
        foreign_keys=[user_id],
        back_populates="friendships_as_user"
    )
    
    friend = relationship(
        "User",
        foreign_keys=[friend_id],
        back_populates="friendships_as_friend"
    )