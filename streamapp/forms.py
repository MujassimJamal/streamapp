from django import forms
from .models import Video
from django.core.exceptions import ValidationError
import os

ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.mov', '.mkv']

def validate_video_format(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in ALLOWED_VIDEO_EXTENSIONS:
        raise ValidationError('Unsupported file extension. Only video files are allowed.')
    
def validate_file_size(value):
    limit_mb = 100
    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(f'File size must not exceed {limit_mb} MB.')

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_path']

    video_path = forms.FileField(
        validators=[validate_video_format, validate_file_size],
        label='Upload Video',
        help_text='Only video files are allowed (mp4, mov, mkv).',
        widget=forms.ClearableFileInput(attrs={
            'accept': '.mp4, .mov, .mkv'
        })
    )