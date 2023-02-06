from shortuuid import ShortUUID


def generate_username():
    return f'user{ShortUUID(alphabet="0123456789").random(length=12)}'
