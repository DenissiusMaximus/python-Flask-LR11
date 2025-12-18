from flask import g


def get_id(func):
    def wrapper(*args, **kwargs):
        try:
            user_id = g.user["id"]["user_id"]
        except:
            user_id = None

        try:
            if user_id:
                return func(user_id, *args, **kwargs)
        finally:
            pass
    return wrapper