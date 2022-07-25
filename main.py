import os
import sys
import pytube

cwd = os.getcwd()

if not os.path.isfile('links.txt'):

    linkstxt = open('links.txt', 'w')
    linkstxt.close()
    print('links.txt not found! It has now been generated, press emter to close the program, and put some links in it.')
    cont = input()
    sys.exit()

linkstxt = open('links.txt', 'r')
links = linkstxt.readlines()
linkstxt.close() 
videos = []

rawfileformat = links[0]

fileformat = rawfileformat.replace('\n', '')

if fileformat == 'mp4':

    print('Downloading as .mp4 file format\n')
    links.remove(rawfileformat)

elif fileformat == 'mp3':

    print('Downloading as .mp3 file format\n')
    links.remove(rawfileformat)

else:

    print('Could not find valid file format, make sure that the file format is in the beginning line of the links.txt, either as "mp4" or "mp3", press enter to close the program')
    cont = input()
    sys.exit()

for i in links:

    try:
    
        p = pytube.Playlist(i)
        print('Found {} videos from playlist "{}"'.format(p.length, p.title))

        for url in p.video_urls:

            videos.append(url)

    except:

        videos.append(i)

print('Attempting to download {} videos\n'.format(len(videos)))
taskscompleted = 0


for i in videos:
    try:

        yt = pytube.YouTube(i)
        fetchsuccess = True

    except:

        print('There was an error in fetching "{}"'.format(i))
        fetchsuccess = False

    if fetchsuccess == True:

        print('Attempting to download "{}"'.format(yt.title))

        try:

            if fileformat == 'mp4':

                streams = yt.streams.filter(progressive=True,)
                streams = streams.desc()
                dstream = streams[0]
                dstream.download(cwd + '\output')

            elif fileformat == 'mp3':

                streams = yt.streams.filter(mime_type='audio/webm')
                streams = streams.desc()
                dstream = streams[0]
                out_file = dstream.download(cwd + '\output')

                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)


            downloadsuccess = True

        except:

            print('There was an error in downloading "{}"'.format(yt.title))
            downloadsuccess = False

        if downloadsuccess == True:

            print('{} "{}" dowloaded succesfully!'.format(fileformat, yt.title))
    
    taskscompleted += 1
    print('{} out of {} tasks completed\n'.format(taskscompleted, len(videos)))
    
print('Done!')
cont=input()     