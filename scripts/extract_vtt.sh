#!/bin/sh
# Extract all subtitle streams from a video file and save them into a .vtt file.

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_file> <output_path>"
    echo "  input_file: The video file to extract subtitles from."
    echo "  output_path: Destination path to save the extracted subtitles."
    exit 1
fi

input_file=$1
output_path=$2

cmd=$(ffmpeg -i "$input_file" 2>&1 | grep -Eo "Stream #[0-9]+:[0-9]+" | grep -Eo "[0-9]+:[0-9]+" | sed 's/\([0-9]\+\):\([0-9]\+\)/\1:s:\2/')

counter=0

for line in $cmd; do
    ffmpeg -i "$input_file" -map "$line"? $output_path/"track$counter.vtt"
    counter=$((counter + 1))
done
