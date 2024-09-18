from django.db import models

class Video(models.Model):
    filename = models.CharField(max_length=255, blank=True)
    thumbnail_path = models.CharField(max_length=255, blank=True)
    video_path = models.FileField(upload_to='videos/')
    subtitle_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.video_path.name
    
class Subtitle(models.Model):
    video = models.ForeignKey(Video, related_name='subtitles', on_delete=models.CASCADE)
    start_time = models.CharField(max_length=25)
    end_time = models.CharField(max_length=25)
    phrase = models.TextField()

    def __str__(self):
        return f"{self.start_time} --> {self.end_time}: {self.phrase}" 