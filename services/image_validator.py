
from PIL import Image
from django.core.exceptions import ValidationError

def image_validation(file):
    max_size = 1024 * 1024 * 2
    if file.size > max_size:
        raise ValidationError("Image file must be under 2MB.")
    
    try:
        im = Image.open(file)
        im.verify()
    except Exception as e:
        raise ValidationError('Invalid or corrupted image file.')
    
    allow_format = {'JPEG', 'PNG', 'WEBP'}
    if im.format not in allow_format:
        raise ValidationError(f"Unsupported image formate. Allow formats: {', '.join(allow_format)}")
    
    file.seek(0)
    

