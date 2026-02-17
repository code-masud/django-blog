import os
import uuid
from django.utils.text import slugify

def seo_upload_path(instance, filename):
    root, ext =os.path.splitext(filename)
    unique_identity = slugify(filename) + '_' + uuid.uuid4().hex
    filename = f'{unique_identity}{ext}'
    return os.path.join('seo', filename)

def logo_upload_path(instance, filename):
    root, ext =os.path.splitext(filename)
    unique_identity = slugify(filename) + '_' + uuid.uuid4().hex
    filename = f'{unique_identity}{ext}'
    return os.path.join('logo', filename)

def avatar_upload_path(instance, filename):
    root, ext =os.path.splitext(filename)
    unique_identity = slugify(filename) + '_' + uuid.uuid4().hex
    filename = f'{unique_identity}{ext}'
    return os.path.join('avatar', filename)

def article_upload_path(instance, filename):
    root, ext =os.path.splitext(filename)
    unique_identity = slugify(filename) + '_' + uuid.uuid4().hex
    filename = f'{unique_identity}{ext}'
    return os.path.join('article', filename)