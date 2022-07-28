import os
import sys
import pytube

cwd = os.getcwd()
faileddowns = 0
successdowns = 0

if not os.path.isfile('links.txt'):

    linkstxt = open('links.txt', 'w')
    linkstxt.write('mp4\ndownload_description=false')
    linkstxt.close()
    print('links.txt not found! It has now been generated, press emter to close the program, and put some links in it.')
    cont = input()
    sys.exit()

linkstxt = open('links.txt', 'r')
links = linkstxt.readlines()
linkstxt.close() 
videos = []

rawfileformat = links[0]
rawdescriptionbool = links[1]

fileformat = rawfileformat.replace('\n', '')
descriptionbool = rawdescriptionbool.replace('download_description=', '')
descriptionbool = descriptionbool.replace('\n', '')

if fileformat == 'mp4':

    print('Downloading as .mp4 file format')
    links.remove(rawfileformat)

elif fileformat == 'mp3':

    print('Downloading as .mp3 file format')
    links.remove(rawfileformat)

else:

    print('Could not find valid file format, make sure that the file format is in the beginning line of the links.txt, either as "mp4" or "mp3", press enter to close the program')
    cont = input()
    sys.exit()

if descriptionbool == 'true':

    print('Downloading description')
    descriptionbool = True
    links.remove(rawdescriptionbool)

elif descriptionbool == 'false':

    print('Not downloading description')
    descriptionbool = False
    links.remove(rawdescriptionbool)

else:
    print('Could not find a valid download_description bool, make sure that it is inputted correctlu: "download_description=("true" or "false")", press enter to close the program')
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
                dstream.download(cwd + '\output\\videos')

            elif fileformat == 'mp3':

                streams = yt.streams.filter(mime_type='audio/webm')
                streams = streams.desc()
                dstream = streams[0]
                out_file = dstream.download(cwd + '\output\\videos')

                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)

            if descriptionbool == True:

                if not os.path.exists(cwd + '\output\descriptions'):
                    
                    os.mkdir(cwd + '\output\descriptions')

                description = yt.description
                descriptiontxt = open(cwd + '\output\descriptions\{}-description.txt'.format(yt.title), 'w')
                descriptiontxt.write(description)
                descriptiontxt.close()
            
            downloadsuccess = True

        except:

            print('There was an error in downloading "{}"'.format(yt.title))
            faileddowns += 1
            downloadsuccess = False

        if downloadsuccess == True:

            successdowns +=1
            print('{} "{}" dowloaded succesfully!'.format(fileformat, yt.title))
    
    taskscompleted += 1
    print('{} out of {} tasks completed\n'.format(taskscompleted, len(videos)))
    
print('Done! {} out of {} downloads sucessful! ({} failed) Press enter to close the program...'.format(successdowns, len(videos), faileddowns))
cont=input()     