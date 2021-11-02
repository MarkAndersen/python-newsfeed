from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
import bcrypt

salt = bcrypt.gensalt()
#very similar to JS models, notice now the columns of the table look very similar in syntax, nullable = NOT NULL or null = false in JS, etc.
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    @validates('email')
    def validate_email(self, key, email):
        # makes sure email address contains @ character
        assert '@' in email

        return email 
    
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 4

        # encrypt password
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    # checks password entered to encrypted password stored
    def verify_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )
