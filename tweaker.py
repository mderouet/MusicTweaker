from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from pydub import AudioSegment
from pathlib import Path
import datetime, os, eyed3, sys, requests, random, os.path
from pyquery import PyQuery
from bs4 import BeautifulSoup

pathToMusicFolder = 'musics/'
musics = []
def clear():
    command = os.popen('clear')
    print(command.read())
def displayBanner(text, bannerType = 0):
    if bannerType == 1:
        print('---------------------------------------------------------------------------------------------------')
        print('|                                                                                                 |')
        print('|                                     ' + text + '                                               |')
        print('|                                                                                                 |')
        print('---------------------------------------------------------------------------------------------------')
    else:
        print('---------------------------------------------------------------------------------------------------')
        print('                                     ' + text + '                                               ')
        print('---------------------------------------------------------------------------------------------------')

clear()
displayBanner('MUSIC TWEAKER', 1)


def scanFolder():
    musics.clear()
    for filename in os.listdir(pathToMusicFolder):
        if not filename.endswith(".DS_Store"):
            musics.append(filename)
    musics.sort()


def clearTags():
    displayBanner('REMOVE METADATA')
    onlyMp3 = True
    for music in musics:
        if not music.lower().endswith('.mp3'):
            onlyMp3 = False
            print('Can only clear tags of mp3 files, convert first audio files to mp3')
            return

    emptyPrint(2)
    for currentMusic in musics:

        mp3 = MP3File(pathToMusicFolder + currentMusic)

        del mp3.song
        del mp3.artist
        del mp3.album
        mp3.year = str(datetime.datetime.now().year)
        del mp3.comment
        del mp3.track
        del mp3.genre

        del mp3.band
        del mp3.composer
        del mp3.copyright
        del mp3.url
        del mp3.publisher

        mp3.set_version(VERSION_BOTH)
        mp3.save()
        tags = mp3.get_tags()

        print(currentMusic + ' tags removed')

    emptyPrint(2)
    choice = input('Would you like to display logs of operation ? Y/N \n')
    if choice.lower() == 'y':
        print(tags)


def emptyPrint(number):
    for var in list(range(number)):
        print()

## here we go bitch
def audioFormatConversion():
    displayBanner('AUDIO FORMAT CONVERSION')
    emptyPrint(2)
    print('Convert everything to :')
    print()
    print('    1. Mp3')
    #print('    2. WAV')
    #print('    3. Flac')
    print()
    choiceFormat = input('Choice : \n')
    emptyPrint(2)
    if int(choiceFormat) == 1:
        for music in musics:
            if music.lower().endswith('.wav'):
                print('Converting ' + music + ' to Mp3 format')
                raw_audio = AudioSegment.from_file(pathToMusicFolder + music, format="raw",frame_rate=44100, channels=2, sample_width=2)
                raw_audio.export(pathToMusicFolder + music.lower().replace('.wav', '.mp3'), format="mp3", bitrate="320k")
                os.remove(pathToMusicFolder + music)
            if music.lower().endswith('.flac'):
                print('Converting ' + music + ' to Mp3 format')
                flac_audio = AudioSegment.from_file(pathToMusicFolder + music, "flac")
                flac_audio.export(pathToMusicFolder + music.lower().replace('.flac', '.mp3'), format="mp3", bitrate="320k")
                os.remove(pathToMusicFolder + music)
            if music.lower().endswith('.mp3'):
                print('Converting ' + music + ' to Mp3 format')
                raw_audio = AudioSegment.from_file(pathToMusicFolder + music, format="raw",frame_rate=44100, channels=2, sample_width=2)
                raw_audio.export(pathToMusicFolder + music, format="mp3", bitrate="320k")
    if choiceFormat == 2:
        print('2')
    if choiceFormat == 3:
        print('3')

def showMusicList():
    displayBanner('List of files to process')
    for music in musics:
        print(music)
    return

def removeAlbumCover():
    displayBanner('REMOVE ALBUM COVER')
    command = os.popen('eyeD3 --remove-all-images ' + pathToMusicFolder + '*.mp3')
    logs = command.read()
    command.close()
    emptyPrint(2)
    print('All album art cover were removed')
    choice = input('Would you like to display logs of operation ? Y/N \n')
    if choice.lower() == 'y':
        print(logs)

def renameFiles():
    songs = []
    for ms in musics:
        if(len(songs) == 0):
            print('Requesting for new song titles...')
            try:
                response = requests.get('https://learnhowtowritesongs.com/wp-content/plugins/song-title-generator/title-function.php')
            except:
                print("Cannot reach learnhowtowritesongs.com, check your internet connection and whether the site is online")
                return
            soup = BeautifulSoup(response.text, 'html.parser')
            html = soup.find('div', id='songTitle').get_text()
            for line in html.splitlines():
                if len(line) > 4:
                    songs.append(line)

        randomSongName = random.choice(songs)
        songs.remove(randomSongName)
        os.rename(pathToMusicFolder + ms, pathToMusicFolder + randomSongName + os.path.splitext(ms)[1])
        print("Renamed file : " + ms + " to " + randomSongName + os.path.splitext(ms)[1])

def menu():
    scanFolder()
    emptyPrint(2)
    print('MENU :')
    print()
    print('    1. Show files')
    print('    2. Remove metadata')
    print('    3. Remove album cover')
    print('    4. Change audio format')
    print('    5. Change file name')
    print('    6. Exit')

    try:
        response = requests.get('https://google.fr/')
    except:
        print("We detected an issue with your internet connection, some features will not work properly")

    emptyPrint(2)
    choice = int(input('Choice : '))
    print(choice)
    if choice == 1:
        clear()
        showMusicList()
    if choice == 2:
        clear()
        clearTags()
    if choice == 3:
        clear()
        removeAlbumCover()
    if choice == 4:
        clear()
        audioFormatConversion()
    if choice == 5:
        clear()
        renameFiles()
    if choice == 6:
        sys.exit()
    menu()
menu()