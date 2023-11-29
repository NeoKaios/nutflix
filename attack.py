import os
import read

filename = 'coca'
input_file = f'movies/{filename}.mp4'
def output_file(i):
    return f'out/{filename}-{i}.mp4'

# Create compressed files
for i in range(23, 51):
    os.system(f'ffmpeg -loglevel quiet -i {input_file} -c:v libx264 -crf {i} {output_file(i)}')

# Reading mark
mark = read.read(input_file)
for i in range(23, 51):
    file = output_file(i)
    print(f'Reading file {file}')
    found = read.read(file)
    if (found and found == mark):
        print(f'SUCC: Found mark in file {i}')
    else:
        print(f'FAIL: Unable to find mark')
