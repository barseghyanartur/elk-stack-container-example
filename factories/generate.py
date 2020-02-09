import argparse
from datetime import timedelta
import sys
from random import randint, sample

from faker import Faker
from freezegun import freeze_time

from logger import LOGGER

__author__ = 'Artur Barseghyan'
__copyright__ = '2020 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'generate_logs',
)


FAKER = Faker()
IDS = set()
MAX_RETRIES = 10


def generate_unique_ids(amount=1000, offset=1):
    return sample(range(offset, amount + offset), amount)


def generate_logs():
    parser = argparse.ArgumentParser(description='Generate logs')
    parser.add_argument(
        '--amount',
        dest="amount",
        default=1000,
        action='store',
        type=int,
        help="Amount of logs to generate",
    )
    parser.add_argument(
        '--offset',
        dest="offset",
        default=1,
        action='store',
        type=int,
        help="Offset of logs to generate",
    )
    args = parser.parse_args(sys.argv[1:])
    amount = args.amount
    offset = args.amount

    milliseconds_delta = timedelta(milliseconds=randint(1, 333))
    delta = timedelta(seconds=15, milliseconds=randint(1, 333))
    unique_ids = generate_unique_ids(amount, offset)
    for id_ in unique_ids:
        created = (
            FAKER.date_time_between(start_date='-10y', end_date='+10y')
            + milliseconds_delta
        )
        classified = created + delta
        explained = classified + delta

        with freeze_time(created):
            LOGGER.info("Created", extra={"id": id_, "success": "true"})

        with freeze_time(classified):
            LOGGER.info("Classified", extra={"id": id_, "success": "true"})

        with freeze_time(explained):
            LOGGER.info("Explained", extra={"id": id_, "success": "true"})


if __name__ == '__main__':
    generate_logs()
