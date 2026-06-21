# SPDX-FileCopyrightText: 2026 OpenAdmin
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class BookToGenre(Base):
    __tablename__ = "book_to_genre"

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"), primary_key=True)


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    bio: Mapped[str | None] = mapped_column(Text)

    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Publisher(Base):
    __tablename__ = "publisher"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    country: Mapped[str | None] = mapped_column(String(100))

    books: Mapped[list["Book"]] = relationship(back_populates="publisher")


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    published_year: Mapped[int | None] = mapped_column()
    summary: Mapped[str | None] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    publisher_id: Mapped[int | None] = mapped_column(ForeignKey("publisher.id"))

    author: Mapped["Author"] = relationship(back_populates="books")
    publisher: Mapped["Publisher | None"] = relationship(back_populates="books")
    genres: Mapped[list["Genre"]] = relationship(
        secondary=BookToGenre.__table__, back_populates="books"
    )
    tag_links: Mapped[list["BookToTag"]] = relationship(
        back_populates="book", cascade="all, delete-orphan"
    )


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    books: Mapped[list["Book"]] = relationship(
        secondary=BookToGenre.__table__, back_populates="genres"
    )


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    book_links: Mapped[list["BookToTag"]] = relationship(back_populates="tag")


class BookToTag(Base):
    __tablename__ = "book_to_tag"

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id"), primary_key=True)
    added_at: Mapped[datetime] = mapped_column(server_default=func.now())

    book: Mapped["Book"] = relationship(back_populates="tag_links")
    tag: Mapped["Tag"] = relationship(back_populates="book_links")
