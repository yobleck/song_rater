import json, os;
from glob import glob;

path = "/home/yobleck/Music/";
types = [".mp3",".m4a",".wav",".ogg",".oga",".wma",".flac",".aac"];

songs = {};
for i in os.walk(path):
    for j in i[2]:
        if(os.path.splitext(j)[-1].lower() in types):
            songs[i[0] + "/" + j] = 0;

f = open("/home/yobleck/Music/song_rater/song_ratings.json","w");
json.dump(songs, f, indent=1);
f.close();
