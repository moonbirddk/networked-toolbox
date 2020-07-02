from filer.fields.file import FilerFileField

class FilerVideoField(FilerFileField):
    default_model_class = 'library.Video'
