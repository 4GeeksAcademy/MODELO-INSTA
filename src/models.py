from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

# Tablas intermedias
post_hashtag = Table(
    "post_hashtag",
    db.metadata,
    Column("post_id", ForeignKey("post.id"), primary_key=True),
    Column("hashtag_id", ForeignKey("hashtag.id"), primary_key=True)
)

reel_hashtag = Table(
    "reel_hashtag",
    db.metadata,
    Column("reel_id", ForeignKey("reel.id"), primary_key=True),
    Column("hashtag_id", ForeignKey("hashtag.id"), primary_key=True)
)


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)
    user_name: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String(20), nullable=False)
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_from = relationship("User", backref="user_from")

    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to = relationship("User", backref="user_to")




class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    caption: Mapped[str] = mapped_column(String(200), nullable=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(backref="post")
    hashtags: Mapped[List["Hashtag"]] = relationship(
        secondary=post_hashtag,
        back_populates="posts"
    )

class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped [int] = mapped_column(primary_key=True)
    comment_text: Mapped [str] = mapped_column(String(200), nullable=True)
    
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    author: Mapped["User"] = relationship("User", backref="comment")
    
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    post: Mapped["Post"] = relationship("Post", backref="comment")

class Reel(db.Model):
    __tablename__ = "reel"

    id: Mapped[int] = mapped_column(primary_key=True)
    caption: Mapped[str] = mapped_column(String(200), nullable=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="reels")

    hashtags: Mapped[List["Hashtag"]] = relationship(
        secondary=reel_hashtag,
        back_populates="reels"
    )

class Media(db.Model):
    __tablename__ ="media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(200), nullable=True)
    url: Mapped[str] = mapped_column(String(100), nullable=True)

    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id"), nullable=False)
    post: Mapped["Post"] =relationship(backref="media")
    


class Hashtag(db.Model):
    __tablename__ = "hashtag"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(30), nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        secondary=post_hashtag,
        back_populates="hashtags"
    )
    reels: Mapped[List["Reel"]] = relationship(
        secondary=reel_hashtag,
        back_populates="hashtags"
    )
