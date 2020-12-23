import json, sys, os;
#https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog

#takes arguments as list of file paths
if(len(sys.argv) > 1):
    f = open("/home/yobleck/Music/song_rater/song_ratings.json","r");
    songs_json = json.load(f);
    f.close();

    song_list = sys.argv[1:];

    for i in song_list:
        if(os.path.isfile(i)):
            if(i not in songs_json):
                songs_json[i] = 0;
                print(i, " added to list");
            else:
                print(i, " is already listed");
        else:
            print(i, " is not a file");

    try:
        f = open("/home/yobleck/Music/song_rater/song_ratings.json","w");
        json.dump(songs_json, f);
        f.close();
    except:
        print("something went wrong with writing to file");
    
else:
    print("no files selected");
