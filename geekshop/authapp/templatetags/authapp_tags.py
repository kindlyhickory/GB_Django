from django import template
from django.conf import settings

register = template.Library()


def avatar_folder(string):
    string = str(string)
    if string.startswith('https'):
        return string
    elif string.startswith('users_avatars'):
        return f'/media/{string}'
    else:
        return '/media/users_avatars/default.jpg'


register.filter('avatar_folder', avatar_folder)
