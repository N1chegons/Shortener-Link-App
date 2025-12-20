class ShortenerBaseError(Exception):
    pass


class NoLongUrlFoundError(ShortenerBaseError):
    pass


class SlugAlreadyExistsError(ShortenerBaseError):
    pass