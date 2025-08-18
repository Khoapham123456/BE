from .user_model import UserModel
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class AdminModel(UserModel):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    user = relationship("UserModel", backref="admin", uselist=False)

    def __repr__(self):
        return f"<Admin id={self.id}, user_id={self.user_id}>"
