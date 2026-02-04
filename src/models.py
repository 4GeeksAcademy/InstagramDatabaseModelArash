from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

# USER TABLE
class User(db.Model):
    __tablename__ = "user"

    # PK = primary key (har user ye id unique dare)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    password: Mapped[str] = mapped_column(String(80), nullable=False)

    # password ro serialize nemikonim (security)
    password: Mapped[str] = mapped_column(String(250), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 1 user -> many posts
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")

    # 1 user -> many comments
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")

    # follower relationships (2 taraf FK darim, pas foreign_keys ro moshakhas mikonim)
    following: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys="Follower.follower_id",
        back_populates="follower_user"
    )

    followers: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys="Follower.following_id",
        back_populates="following_user"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }


# POST TABLE
class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # FK = foreign key (in post male kodoom user-e?)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # relationship baraye dastresi be user
    author: Mapped["User"] = relationship("User", back_populates="posts")

    # 1 post -> many comments
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "image_url": self.image_url,
            "caption": self.caption,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id
        }


# COMMENT TABLE
class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # FK ha
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    # relationship ha
    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
            "post_id": self.post_id
        }


# FOLLOWER TABLE  (many-to-many for User <-> User)
class Follower(db.Model):
    __tablename__ = "follower"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # follower_id = kasi ke follow mikone
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # following_id = kasi ke follow mishe
    following_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # in constraint jaloye duplicate follow ro migire (mesle: Ali do bar Reza ro follow nakone)
    __table_args__ = (
        UniqueConstraint("follower_id", "following_id", name="unique_follow_pair"),
    )

    # relationship ha baraye access be user object
    follower_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="following"
    )

    following_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[following_id],
        back_populates="followers"
    )

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "following_id": self.following_id,
            "created_at": self.created_at.isoformat()
        }