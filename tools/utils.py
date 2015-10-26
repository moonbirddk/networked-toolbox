import uuid


def generate_upload_path(instance, filename, dirname=None):
    """
        Generate random path name for file.
        @see https://docs.djangoproject.com/en/1.8/ref/models/fields/#django.db.models.FileField.upload_to
    """
    ext = filename.split('.')[-1]
    rand_name = "{}.{}".format(uuid.uuid4().hex, ext)
    if dirname:
        rand_name = "{}/{}".format(dirname, rand_name)
    return rand_name
