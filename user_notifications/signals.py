''' Django notifications signal file '''
# -*- coding: utf-8 -*-
from django.dispatch import Signal

notify = Signal(providing_args=[     
    'recipient',
    'actor',
    'verb', 
    'target', 
    'description',
    'timestamp', 
    'level'
])
