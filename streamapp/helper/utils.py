from django.conf import settings
import subprocess
import os
import shutil
import re
import pycountry
from langdetect import detect

def process_video(video, Subtitle):
    video_path = settings.MEDIA_ROOT / video.video_path.name
    
    file_basename = os.path.basename(video_path)
    filename = file_basename.split('.')[0]
    
    thumbnail_path = 'thumbnails/' + filename + '.png'
    thumbnail_base_path = settings.MEDIA_ROOT / thumbnail_path
    
    subtitle_base_path = settings.MEDIA_ROOT / 'subtitles'
    
    create_thumbnail(video_path, thumbnail_base_path)
    subtitle_data, merged_subtitles = extract_subtitle(video_path, subtitle_base_path)

    # Store individual subtitles in the Subtitle model
    if subtitle_data:
        for subtitle in subtitle_data:
            Subtitle.objects.create(
                video=video,
                start_time=subtitle['start_time'],
                end_time=subtitle['end_time'],
                phrase=subtitle['phrase']
            )

    # Update model fields with new values
    video.filename = file_basename
    video.thumbnail_path = thumbnail_path
    video.subtitle_text = merged_subtitles
    video.save()

def create_dir(directory, exist_ok=True):
    os.makedirs(directory, exist_ok=True)

def remove_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

def remove_file(file):
    if os.path.exists(file):
        os.remove(file)

def extract_subtitle(video_path, save_to):
    # Create temporary subtitle path, actual saving will occur in database
    create_dir(save_to)
    subtitle_text = ''
    subtitle_data = None
    try:
       subtitle_filename = 'subtitles.vtt'
       ffmpeg = ['sh', '/app/scripts/extract_vtt.sh', video_path, save_to]
       cat = [f'cat {save_to}/*.vtt > {save_to}/{subtitle_filename}']
       subprocess.run(ffmpeg, check=True)
       subprocess.run(cat, shell=True, check=True)
       
       # Read the extracted subtitles
       with open(save_to/subtitle_filename, 'r', encoding='utf-8') as file:
           subtitle_text = file.read()
           file.close()
           
       # Parse subtitle data from the merged file
       subtitle_data = parse_vtt_file(save_to/subtitle_filename)
    except subprocess.CalledProcessError as e:
        print(f"Error extracting subtitles: {e}")
    
    remove_dir(save_to)
    return subtitle_data, subtitle_text

def create_thumbnail(video_path, save_to):
    create_dir(os.path.dirname(save_to))
    try:
       cmd = ['ffmpeg', '-i', video_path, '-ss', '00:00:10.000', '-update', 'true', '-vframes', '1', save_to]
       result = subprocess.run(cmd, check=True) 
    except subprocess.CalledProcessError as e:
        print(f"Error generating thumbnail: {e}")

def serve_subtitles(subtitles):
    tmp_name = 'tmp'
    tmp_dir = settings.MEDIA_ROOT / tmp_name
    remove_dir(tmp_dir)
    create_dir(tmp_dir)

    raw_sections = re.split(r'WEBVTT', subtitles)
    total_tracks = len(raw_sections) - 1
    lang_sections = [section.strip() for section in raw_sections if section.strip()]
    tracks = []
    
    for i in range(total_tracks):
        content = "WEBVTT\n\n" + lang_sections[int(i)]
        tmp_file = tmp_dir / f'track{i}.vtt'
        with open(tmp_file, 'w+') as file:
            file.write(content)
            file.close()
        filename = detect_language(tmp_file) + f"-{i}.vtt"
        tracks.append(filename)
        shutil.move(tmp_file, tmp_dir / filename)
    
    return (tracks, tmp_name)

def parse_vtt_file(file_path):
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split by "WEBVTT" headers to separate different tracks
    tracks = content.split('WEBVTT')

    # Process each track
    for track in tracks:
        lines = track.strip().split('\n')
        if not lines:
            continue
        
        i = 0
        while i < len(lines):
            if '-->' in lines[i]:
                time_range = lines[i]
                i += 1
                subtitle_text = ""
                
                while i < len(lines) and lines[i] and '-->' not in lines[i]:
                    subtitle_text += lines[i] + ' '
                    i += 1
                
                # Save the subtitle entry
                subtitles.append({
                    'start_time': time_range.split(' --> ')[0],
                    'end_time': time_range.split(' --> ')[1],
                    'phrase': subtitle_text.strip()
                })
            else:
                i += 1
    
    return subtitles

def detect_language(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    lang_code = detect(content)
    lang = pycountry.languages.get(alpha_2=lang_code)

    if lang:
        return lang.name
    return 'Unknown'