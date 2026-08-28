from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from hios.db.models.memory_entry import MemoryRecord


class MemoryRepository:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def save(
        self,
        record: MemoryRecord,
    ) -> MemoryRecord:

        self._session.add(record)

        await self._session.commit()

        await self._session.refresh(record)

        return record

    async def retrieve(
        self,
        query: str,
    ) -> list[MemoryRecord]:

        stmt = (
            select(MemoryRecord)
            .where(
                MemoryRecord.description.ilike(
                    f"%{query}%"
                )
            )
        )

        result = await self._session.execute(
            stmt,
        )

        return list(
            result.scalars().all()
        )

    async def search_similar(
        self,
        embedding: list[float],
        limit: int = 5,
        threshold: float = 0.70,
        category: str | None = None,
    ) -> list[MemoryRecord]:

        distance = MemoryRecord.embedding.cosine_distance(
            embedding
        )

        stmt = (
            select(MemoryRecord)
            .where(
                MemoryRecord.embedding.is_not(None),
                distance <= (1 - threshold),
            )
        )

        if category is not None:
            stmt = stmt.where(
                MemoryRecord.category == category,
            )

        stmt = (
            stmt
            .order_by(distance)
            .limit(limit)
        )

        result = await self._session.execute(stmt)

        return list(result.scalars().all())

    async def list(
        self,
    ) -> list[MemoryRecord]:

        stmt = select(
            MemoryRecord,
        )

        result = await self._session.execute(
            stmt,
        )

        return list(
            result.scalars().all()
        )

    async def delete(
        self,
        record: MemoryRecord,
    ):

        await self._session.delete(
            record,
        )

        await self._session.commit()