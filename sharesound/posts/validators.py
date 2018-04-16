import os
from django.core.exceptions import ValidationError

def validate_audiofile_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = get_valid_audio_extensions()
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file format')
        
def get_valid_audio_extensions():
    return ['.mp3', '.wav']
