from types import NoneType
from sqlalchemy.orm import Session
from sqlalchemy import select
from markupsafe import escape
from models import Utilisateur, engine
from argon2 import PasswordHasher
from flask_jwt_extended import create_access_token

class UtilisateurController():

    def __init__(self) -> None:
        self.ph = PasswordHasher()

    def addUser(self,email:str,pseudo:str,password:str,role:int) -> None:
        with Session(engine) as session:
            newUser = Utilisateur(
                email=email,
                pseudo=pseudo,
                password=self.ph.hash(password),
                role=role
            )
            session.add(newUser)
            session.commit()

    def deleteUser(self,id:int) -> None:
        session = Session(engine)
        query = select(Utilisateur).where(Utilisateur.id.in_([id]))
        for user in session.scalars(query):
            session.delete(user)
            session.commit()

    def getUser(self,id:int):
        session = Session(engine)
        query = select(Utilisateur).where(Utilisateur.id.in_([id]))
        users = []
        result = session.scalars(query)
        for user in result:
            users.append({
                "id": user.id,
                "email": user.email,
                "pseudo": user.pseudo,
                "role": user.role,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at if type(user.updated_at) == NoneType else user.updated_at.isoformat()
            })
        return users
    
    def updateUser(self,id:int,data:dict):
        session = Session(engine)
        query = select(Utilisateur).where(Utilisateur.id.in_([id]))
        for user in session.scalars(query):
            for index in data:
                if(index == "email"):
                    user.email = escape(data["email"])
                if(index == "pseudo"):
                    user.pseudo = escape(data["pseudo"])
                if(index == "password"):
                    user.password = self.ph.hash(escape(data["password"]))
                if(index == "role"):
                    user.role = escape(data["role"])
        session.commit()
    
    def login(self, data:dict):
        session = Session(engine)
        query = select(Utilisateur).where(Utilisateur.email.in_([data["email"]]))
        result = session.scalars(query)
        for user in result:
            if self.ph.verify(user.password, data["password"]) :
                token = create_access_token(
                    identity={
                        "id": user.id,
                        "email": user.email,
                        "pseudo": user.pseudo,
                        "role": user.role
                    }
                )
        return token