PAGE_SIZE = 50

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'Movies.components.paginator.CustomLimitOffsetPagination',
    'PAGE_SIZE': PAGE_SIZE,
}
