from faker import Faker
from logger import LOGGER

__author__ = 'Artur Barseghyan'
__copyright__ = '2020 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'generate_logs',
)


def generate_logs():
    faker = Faker()
    for i in range(1000):
        id_ = faker.pyint()
        LOGGER.info("Created", extra={"id": id_})
        LOGGER.info("Classified", extra={"id": id_})
        LOGGER.info("Explained", extra={"id": id_})


if __name__ == '__main__':
    generate_logs()
