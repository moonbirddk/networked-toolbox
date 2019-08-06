def get_one_to_one_field_names(model_instance): 
    return [obj for obj in model_instance._meta.fields if obj.__class__.one_to_one]
