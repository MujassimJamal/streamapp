from django.shortcuts import render, redirect
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse
from .forms import VideoUploadForm
from .models import Video, Subtitle
from .helper.utils import *

def home(request):
    videos = Video.objects.all()
    form = VideoUploadForm()

    context = {
        'videos': videos,
        'form' : form,
        'vs_visibility' : False,
    }
    return render(request, 'home.html', context)

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            process_video(video, Subtitle)
            return redirect('home')
        else:
            context = {'form': form}
            return render(request, 'error.html', context)
    return HttpResponseBadRequest("<h1>Bad request!!!</h1>")

def fetch_video(request, video_id):
    if request.method == "POST":
        video = get_object_or_404(Video, id=video_id)
        
        subtitles = video.subtitle_text
        tracks, tmp_name = serve_subtitles(subtitles)
        tmp_dir = '/media/' + tmp_name

        context = {
            'videos' : Video.objects.all(),
            'form' : VideoUploadForm(),
            'vs_visibility' : True,
            'total_tracks' : len(tracks),
            'video': video,
            'tmp_dir': tmp_dir,
            'track_numbers' : range(len(tracks)),
            'tracks' : tracks,
        }
        return render(request, 'home.html', context)
    return HttpResponseBadRequest("<h1>Bad request!!!</h1>")

def delete_video(request, video_id):
    if request.method == "POST":
        video = get_object_or_404(Video, id=video_id)
        
        thumbnail_path = video.thumbnail_path
        video_path = str(video.video_path)
        media_path = settings.MEDIA_ROOT
        
        remove_file(media_path / thumbnail_path)
        remove_file(media_path / video_path)
        remove_dir(media_path / 'tmp')
        video.delete()
        
        return redirect('home')
    
    return HttpResponseBadRequest("<h1>Bad request!!!</h1>")

def search_subtitles(request):
    query = request.GET.get('q', '')
    video_id = request.GET.get('video_id', '')

    if query and video_id:
        matching_subtitles = Subtitle.objects.filter(
            video_id=video_id,
            phrase__icontains=query
        )

        # To prevent duplicate subtitles, for e.g. US and UK based subtitles are mostly the same.
        unique_item = set()
        results = []
        for subtitle in matching_subtitles:
            if subtitle.phrase not in unique_item:
                results.append(
                {
                    'id': subtitle.id,
                    'phrase': subtitle.phrase,
                    'start_time': subtitle.start_time
                })
                unique_item.add(subtitle.phrase)
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})
