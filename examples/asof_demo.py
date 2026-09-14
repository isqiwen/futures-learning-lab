"""Point-in-time selection with known publication AND historical receipt times."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import math


def aware(value: datetime) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError('timezone-aware datetime required')


@dataclass(frozen=True)
class Observation:
    series: str
    period: str
    value: float
    published_at: datetime
    received_at: datetime
    revision: int

    def __post_init__(self) -> None:
        aware(self.published_at); aware(self.received_at)
        if not self.series or not self.period or not math.isfinite(self.value):
            raise ValueError('valid series, period and finite value required')
        if isinstance(self.revision, bool) or not isinstance(self.revision, int) or self.revision < 0:
            raise ValueError('nonnegative integer revision required')
        if self.received_at < self.published_at:
            raise ValueError('receipt earlier than publication requires provenance review')

    @property
    def available_at(self) -> datetime:
        return max(self.published_at, self.received_at)


def select_asof(rows: list[Observation], decision_at: datetime) -> dict[tuple[str, str], Observation]:
    """Latest eligible revision for each series/reference period. Fail on conflicts."""
    aware(decision_at)
    result: dict[tuple[str, str], Observation] = {}
    identities = {}
    for row in rows:
        identity = (row.series, row.period, row.revision)
        if identity in identities and identities[identity] != row:
            raise ValueError(f'conflicting revision: {identity}')
        identities[identity] = row
        if row.available_at > decision_at:
            continue
        key = (row.series, row.period)
        old = result.get(key)
        if old is None or row.revision > old.revision:
            result[key] = row
    return result


def demo_rows() -> list[Observation]:
    dt = datetime.fromisoformat
    return [
        Observation('SYNTHETIC_INVENTORY', '2026-08', 100.0,
                    dt('2026-09-01T09:00:00+08:00'), dt('2026-09-01T09:00:05+08:00'), 0),
        Observation('SYNTHETIC_INVENTORY', '2026-08', 110.0,
                    dt('2026-09-08T09:00:00+08:00'), dt('2026-09-08T09:00:05+08:00'), 1),
    ]


def main() -> None:
    decision = datetime.fromisoformat('2026-09-02T10:00:00+08:00')
    print('SYNTHETIC TEACHING DATA — historical receipt times are explicitly supplied.')
    print('Decision time:', decision.isoformat())
    for key, row in select_asof(demo_rows(), decision).items():
        print(key, 'value=', row.value, 'revision=', row.revision)
    print('A latest-value table would wrongly inject the later revision 110 into this decision.')
    print('Downloading historical data today does not establish its historical receipt timestamp.')


if __name__ == '__main__':
    main()
