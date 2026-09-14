"""IID-noise parameter-search demonstration; neither annualized Sharpe nor real PnL."""
from __future__ import annotations
import math
import random
import statistics


def run_experiment(trials: int, *, samples: int = 120, repetitions: int = 30,
                   seed: int = 20260914) -> dict[str, float | int]:
    for value, minimum in [(trials, 1), (samples, 2), (repetitions, 1)]:
        if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
            raise ValueError('invalid integer experiment size')
    rng = random.Random(seed)
    selected_in, selected_out = [], []
    for _ in range(repetitions):
        candidate_scores, out_scores = [], []
        for _ in range(trials):
            train = [rng.gauss(0, 1) for _ in range(samples)]
            test = [rng.gauss(0, 1) for _ in range(samples)]
            # mean / standard error, used only as a selection score here.
            candidate_scores.append(statistics.mean(train) / (statistics.stdev(train) / math.sqrt(samples)))
            out_scores.append(statistics.mean(test) / (statistics.stdev(test) / math.sqrt(samples)))
        winner = max(range(trials), key=candidate_scores.__getitem__)
        selected_in.append(candidate_scores[winner])
        selected_out.append(out_scores[winner])
    return {'trials': trials, 'mean_selected_in_sample_score': statistics.mean(selected_in),
            'mean_selected_out_of_sample_score': statistics.mean(selected_out),
            'repetitions': repetitions, 'seed': seed}


def main() -> None:
    print('SYNTHETIC IID NOISE — no skill, market returns, costs or executable strategy.')
    for trials in [1, 10, 100]:
        print(run_experiment(trials))
    print('This fixed-seed illustration is not a DSR/PBO implementation or proof of any trading edge.')
    print('Repeat seeds and report uncertainty; do not pick only the most persuasive realization.')


if __name__ == '__main__':
    main()
