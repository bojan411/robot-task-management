from zoneinfo import ZoneInfo
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP


class TimestampedModel(object):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        DateTime(timezone=True), default=datetime.now(tz=ZoneInfo("UTC"))
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo("UTC")),
        onupdate=datetime.now(tz=ZoneInfo("UTC")),
    )
