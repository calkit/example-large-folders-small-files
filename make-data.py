#!/usr/bin/env python3
"""Create some data."""
from pathlib import Path
import random
import shutil
import string

NUM_FILES = 6000
TOTAL_MB = 600
TOTAL_BYTES = TOTAL_MB * 1024 * 1024  # 600 MiB
OUTPUT_DIR = Path("results")
RANDOM_SEED_OFFSET = 2


def random_block(rng: random.Random, size: int) -> bytes:
    # Keep output as readable text while varying content between files
    alphabet = string.ascii_letters + string.digits + "     \n"
    return "".join(rng.choices(alphabet, k=size)).encode("utf-8")


def main() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    base_size = TOTAL_BYTES // NUM_FILES
    remainder = TOTAL_BYTES % NUM_FILES

    total_written = 0

    for i in range(NUM_FILES):
        target_size = base_size + (1 if i < remainder else 0)
        file_path = OUTPUT_DIR / f"file_{i + 1:04d}.txt"

        # Seed per file index for deterministic but distinct content
        rng = random.Random(i + 1 + RANDOM_SEED_OFFSET)

        # Write in chunks to avoid building large strings in memory
        chunk_size = 8192
        remaining = target_size

        with file_path.open("wb") as f:
            while remaining > 0:
                n = min(chunk_size, remaining)
                f.write(random_block(rng, n))
                remaining -= n

        total_written += target_size

    print(f"Created {NUM_FILES} files in '{OUTPUT_DIR}'.")
    print(
        f"Total bytes written: {total_written} "
        f"({total_written / (1024 * 1024):.2f} MiB)"
    )


if __name__ == "__main__":
    main()
