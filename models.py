from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, func, ForeignKey, create_engine
import datetime
from typing_extensions import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]
timestamp_create = Annotated[datetime.datetime, mapped_column(nullable=False, default=func.CURRENT_TIMESTAMP())]
timestamp_update = Annotated[datetime.datetime, mapped_column(nullable=True, server_onupdate=func.CURRENT_TIMESTAMP())]
engine = create_engine("sqlite:///bdd.db", echo=True)

class Base(DeclarativeBase):
    pass

class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(String(255), unique=True)
    pseudo: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[timestamp_create]
    updated_at: Mapped[timestamp_update]

class Post(Base):
    __tablename__ = "post"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(255), unique=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[timestamp_create]
    updated_at: Mapped[timestamp_update]
    userId: Mapped[int] = mapped_column(ForeignKey("utilisateur.id"))

class Picture(Base):
    __tablename__ = "picture"

    id: Mapped[intpk]
    url: Mapped[str] = mapped_column(Text, unique=True)
    alt: Mapped[str] = mapped_column(Text)
    postId: Mapped[int] = mapped_column(ForeignKey("post.id"))

class Commentaire(Base):
    __tablename__ = "commentaire"

    id: Mapped[intpk]
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[timestamp_create]
    updated_at: Mapped[timestamp_update]
    userId: Mapped[int] = mapped_column(ForeignKey("utilisateur.id"))
    postId: Mapped[int] = mapped_column(ForeignKey("post.id"))