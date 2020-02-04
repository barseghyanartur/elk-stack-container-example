import argparse
from datetime import timedelta
import sys
from uuid import uuid4

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
MAX_RETRIES = 3


def unique_id(retries=0):
    id_ = FAKER.pyint()
    if id_ not in IDS:
        IDS.add(id_)
        return id_
    else:
        retries += 1
        if retries > MAX_RETRIES:
            return uuid4()
        return unique_id(retries)


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
    args = parser.parse_args(sys.argv[1:])
    amount = args.amount

    delta = timedelta(seconds=15)
    for i in range(amount):
        id_ = unique_id()

        created = FAKER.date_time_between(start_date='-10y', end_date='+10y')
        classified = created + delta
        explained = classified + delta

        with freeze_time(created):
            LOGGER.info("Created", extra={"id": id_})

        with freeze_time(classified):
            LOGGER.info("Classified", extra={"id": id_})

        with freeze_time(explained):
            LOGGER.info("Explained", extra={"id": id_})


if __name__ == '__main__':
    generate_logs()
