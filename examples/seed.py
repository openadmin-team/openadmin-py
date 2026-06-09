import random

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from . import models

fake = Faker()

GENRES = [
    'Fiction', 'Non-Fiction', 'Mystery', 'Thriller', 'Science Fiction',
    'Fantasy', 'Romance', 'Horror', 'Biography', 'History',
    'Self-Help', 'Travel', 'Cooking', 'Science', 'Philosophy',
    'Poetry', 'Drama', 'Children', 'Young Adult', 'Graphic Novel',
]

TAGS = [
    'bestseller', 'award-winner', 'classic', 'debut', 'series',
    'standalone', 'illustrated', 'translated', 'adapted', 'hardcover',
    'paperback', 'audiobook', 'ebook', 'signed', 'limited-edition',
    'out-of-print', 'new-release', 'staff-pick', 'book-club', 'recommended',
]


async def seed(engine: AsyncEngine) -> None:
    session_factory = async_sessionmaker(engine, class_=AsyncSession)

    async with session_factory() as session:
        genres = [models.Genre(name=name) for name in GENRES]
        session.add_all(genres)

        tags = [models.Tag(name=name) for name in TAGS]
        session.add_all(tags)

        publishers = [
            models.Publisher(
                name=fake.company(),
                country=fake.country(),
            )
            for _ in range(20)
        ]
        session.add_all(publishers)

        authors = [
            models.Author(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                bio=fake.paragraph(nb_sentences=3) if random.random() > 0.2 else None,
            )
            for _ in range(30)
        ]
        session.add_all(authors)

        await session.flush()

        books = [
            models.Book(
                title=fake.sentence(nb_words=random.randint(2, 6)).rstrip('.'),
                published_year=random.randint(1900, 2025) if random.random() > 0.1 else None,
                summary=fake.paragraph(nb_sentences=random.randint(2, 5)) if random.random() > 0.15 else None,
                author_id=random.choice(authors).id,
                publisher_id=random.choice(publishers).id if random.random() > 0.1 else None,
            )
            for _ in range(100)
        ]
        session.add_all(books)

        await session.flush()

        for book in books:
            book.genres.extend(random.sample(genres, k=random.randint(1, 3)))
            for tag in random.sample(tags, k=random.randint(0, 4)):
                session.add(models.BookToTag(book_id=book.id, tag_id=tag.id))

        await session.commit()
