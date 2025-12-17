from __future__ import annotations

import hashlib
import random
from typing import Iterable, Sequence, Tuple, TypeVar

T = TypeVar("T")


def _hash_u64(data: bytes) -> int:
    # Use sha256 and take first 8 bytes as an integer
    h = hashlib.sha256(data).digest()
    return int.from_bytes(h[:8], byteorder="big", signed=False)


def cluster_seed(world_seed: int, cx: int, cy: int) -> int:
    payload = world_seed.to_bytes(8, "big", signed=False) + cx.to_bytes(8, "big", signed=True) + cy.to_bytes(8, "big", signed=True)
    return _hash_u64(payload)


def cluster_rng(world_seed: int, cx: int, cy: int) -> random.Random:
    return random.Random(cluster_seed(world_seed, cx, cy))


def weighted_choice(rng: random.Random, items: Sequence[T], weights: Sequence[float]) -> T:
    assert len(items) == len(weights) and len(items) > 0
    total = sum(weights)
    r = rng.random() * total
    acc = 0.0
    for item, w in zip(items, weights):
        acc += w
        if r <= acc:
            return item
    return items[-1]


def choose_n_unique(rng: random.Random, population: Sequence[T], n: int) -> Sequence[T]:
    n = max(0, min(n, len(population)))
    return rng.sample(list(population), n)
