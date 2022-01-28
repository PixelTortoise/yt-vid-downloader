go = False
go1 = False
go2 = False

try:
    from pytube import YouTube
    go1 = True

except:
    print('Could not import pytube module! This is a required module for this to run, to install it simply put "pip install pytube" in the windows command line.\nI have no idea what it is for mac or linux, figure it out.\n')
    cont = input()
    
if go1 == True:
    
    try:
        links = open('links.txt', 'r')
        print('Found links.txt!\n')
        go2 = True

    except:
        print('No links.txt found! Creating one in current directory...')
        links = open('links.txt', 'w')
        links.close
        print('Created new links.txt!\n')
        print('Restart program and put youtube links that you want to download inside of it, then restart the program.')
        cont = input()

if go1 == True:
    if go2 == True:
        go = True

if go == True:

    for i in links:
        try:
            yt = YouTube(i)
            title = yt.title

        except:
            print('Connection Error!')

        print("Downloading video: %s" % title)

        stream = yt.streams.filter(file_extension = 'mp4', progressive=True)
    
        try:
            stream = stream.last()
            stream.download(output_path = 'downlaods/')
            print('Finished downloading video: %s\n' % title)

        except:
            print('Error Downloading Video!\n')

    links.close()

    print('Done!')
    cont = input()

    
    
    
    

