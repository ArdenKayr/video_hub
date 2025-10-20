# apps/core/validators.py

"""
Custom validators for use across the project.
"""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os


def validate_file_size(file, max_size_mb: int = 5):
    """
    Validate file size.
    
    Args:
        file: File object to validate
        max_size_mb: Maximum file size in megabytes
        
    Raises:
        ValidationError: If file size exceeds maximum
    """
    max_size = max_size_mb * 1024 * 1024  # Convert MB to bytes
    if file.size > max_size:
        raise ValidationError(
            _(f'File size cannot exceed {max_size_mb}MB.')
        )


def validate_image_extension(file):
    """
    Validate that file is an image.
    
    Args:
        file: File object to validate
        
    Raises:
        ValidationError: If file is not a valid image
    """
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ext = os.path.splitext(file.name)[1].lower()
    
    if ext not in valid_extensions:
        raise ValidationError(
            _('Only image files are allowed (jpg, jpeg, png, gif, webp).')
        )


def validate_video_extension(file):
    """
    Validate that file is a video.
    
    Args:
        file: File object to validate
        
    Raises:
        ValidationError: If file is not a valid video
    """
    valid_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    ext = os.path.splitext(file.name)[1].lower()
    
    if ext not in valid_extensions:
        raise ValidationError(
            _('Only video files are allowed (mp4, avi, mov, mkv, webm).')
        )