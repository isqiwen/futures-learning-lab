"""Synthetic futures accounting examples, not exchange rules or a trading engine."""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal

D = Decimal


def finite(value: Decimal, label: str) -> Decimal:
    if not isinstance(value, Decimal) or not value.is_finite():
        raise ValueError(f'{label} must be a finite Decimal')
    return value


@dataclass(frozen=True)
class Contract:
    symbol: str
    multiplier: Decimal
    tick_size: Decimal

    def __post_init__(self) -> None:
        if not self.symbol:
            raise ValueError('symbol is required')
        for name in ['multiplier', 'tick_size']:
            if finite(getattr(self, name), name) <= 0:
                raise ValueError(f'{name} must be positive')

    @property
    def tick_value(self) -> Decimal:
        return self.multiplier * self.tick_size


def pnl(contract: Contract, entry: Decimal, exit: Decimal, signed_quantity: int,
        total_fees: Decimal = D('0')) -> Decimal:
    """Lifetime gross PnL less explicitly supplied total fees. Negative quantity = short.

    This is NOT a daily settlement cash-flow ledger. Caller owns trade timing,
    actual fill prices, per-leg fees, contract selection, and execution constraints.
    """
    finite(entry, 'entry'); finite(exit, 'exit'); finite(total_fees, 'total_fees')
    if not isinstance(signed_quantity, int) or isinstance(signed_quantity, bool):
        raise ValueError('signed_quantity must be an integer')
    if total_fees < 0:
        raise ValueError('total_fees must be nonnegative')
    # Negative futures prices are intentionally not rejected by this generic helper.
    return (exit - entry) * contract.multiplier * signed_quantity - total_fees


def illustrative_margin(price: Decimal, quantity: int, contract: Contract,
                        margin_rate: Decimal) -> Decimal:
    """Simplified positive-price classroom example; not a broker margin calculator."""
    finite(price, 'price'); finite(margin_rate, 'margin_rate')
    if price <= 0 or margin_rate <= 0 or margin_rate > 1:
        raise ValueError('requires positive price and 0 < margin_rate <= 1')
    if not isinstance(quantity, int) or isinstance(quantity, bool):
        raise ValueError('quantity must be an integer')
    return price * abs(quantity) * contract.multiplier * margin_rate


def roll_example() -> dict[str, Decimal]:
    near = Contract('DEMO_NEAR', D('10'), D('1'))
    far = Contract('DEMO_FAR', D('10'), D('1'))
    # Buy near at 100, sell near at 101, buy far at 111, sell far at 112.
    actual = pnl(near, D('100'), D('101'), 1) + pnl(far, D('111'), D('112'), 1)
    # WRONG: interpret a price discontinuity in a spliced series as a holding return.
    incorrect = (D('112') - D('100')) * near.multiplier
    return {'contract_level_gross_pnl': actual, 'incorrect_spliced_pnl': incorrect,
            'artificial_difference': incorrect - actual}


def main() -> None:
    print('SYNTHETIC TEACHING DATA — not real contracts, fees, or strategy evidence.')
    print(roll_example())
    contract = Contract('DEMO', D('10'), D('1'))
    print('Hypothetical tick value:', contract.tick_value)
    print('Hypothetical margin:', illustrative_margin(D('100'), 1, contract, D('0.1')))
    print('Margin is collateral, not the default denominator of portfolio return.')
    print('Real implementation additionally needs daily settlement, fills, costs and risk rules.')


if __name__ == '__main__':
    main()
