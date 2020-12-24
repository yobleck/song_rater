import json, random, time;
from datetime import datetime; #for logging
import sys, tty, termios; #for user input
import multiprocessing, playsound; #for playing songs

cwd = sys.path[0];

#open json file with song names and scores
f = open(cwd + "/song_ratings.json","r");
songs = json.load(f);
f.close();
songs_as_list = list(songs);


#save songs to json
def save():
    f = open(cwd + "/song_ratings.json","w");
    json.dump(songs, f, indent=1);
    f.close();


#user input function
def getch():
    fd = sys.stdin.fileno();
    old_settings = termios.tcgetattr(fd);
    try:
        tty.setcbreak(fd);
        ch = sys.stdin.read(1);
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings);
    return ch;

gen_new_pair = True;


#stop sound from playing
def kill_audio():
    try:
        audio.kill();
        audio.join();
    except:
        pass;


#logging via decorator function
logging = False;
if(logging):
    log = open(cwd + "/log.txt","a");log.write("\n" + str(datetime.now().isoformat()) + " LOGGING STARTED\n");log.close();
    def logger(func):
        def inner(*args, **kwargs):
            log = open(cwd + "/log.txt","a");
            log.write(str(datetime.now().isoformat())+" func: "+str(func.__qualname__)+" *args: "+str(args)+" **kwargs: "+str(kwargs)+"\n");
            log.close(); #TODO: how to list return value without calling code twice?
            return func(*args, **kwargs);
        return inner;
    
    save = logger(save);
    kill_audio = logger(kill_audio);
    getch = logger(getch);
    print = logger(print);
            

print("esc or q to quit.\n1 or 2 to choose song (c to skip)\n[ or ] to play 1 or 2 (p or backspace to stop)");print("\n\n\n");

while(True):
    
    #display new pair of songs
    if(gen_new_pair):
        while(True):
            song1 = random.choice(songs_as_list);
            song2 = random.choice(songs_as_list);
            if(song1 != song2): #make sure not same song
                break;
        gen_new_pair = False;
        print("\033[F\033[F\033[F\33[2K1.) " + str(song1.split("/")[-1])[:70] + "\nor\n\33[2K2.) " + str(song2.split("/")[-1])[:70]);
        #print("\r\33[2K",end="");
        #60 hardcoded to my konsole size
    
    #user input duh
    usr_input = getch();
    print(usr_input,end="\n\033[F");
    
    
    if(usr_input in ["q", "\x1b"]): #esc or q and key up
        save();
        kill_audio();
        break;
    
    ###pick a song###
    
    if(usr_input == "1"):
        songs[song1] += 1;
        save();
        kill_audio();
        gen_new_pair = True;
    
    if(usr_input == "2"):
        songs[song2] += 1;
        save();
        kill_audio();
        gen_new_pair = True;
    
    if(usr_input == "c"): #c to skip comparison and gen new pair
        kill_audio();
        gen_new_pair = True;
    
    ###play a song###
    
    if(usr_input == "["): #[ to play song 1
        kill_audio();
        audio = multiprocessing.Process(target=playsound.playsound, args=(song1,));
        #audio.daemon = True;
        audio.start();
    
    if(usr_input == "]"): #] to play song 2
        kill_audio();
        audio = multiprocessing.Process(target=playsound.playsound, args=(song2,));
        #audio.daemon = True;
        audio.start();
    
    if(usr_input in ["p", "\x08", "\b", "\x7f"]): #backspace or p to stop song
        kill_audio();
    
#end while loop
save(); #just in case
print("\33[2K"); #clear last line so terminal prompt behaves properly on exit
