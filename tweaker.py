from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from pydub import AudioSegment
import datetime, os, eyed3, sys


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



for filename in os.listdir(pathToMusicFolder):
    if not filename.endswith(".DS_Store"): 
        musics.append(filename)


def clearTags():
    emptyPrint(2)
    displayBanner('REMOVE METADATA')
    emptyPrint(3)
    artistName = input("Artist name : ")
    albumTitle = input("Album title : ")
    for currentMusic in musics:

        mp3 = MP3File(pathToMusicFolder + currentMusic)

        del mp3.song
        mp3.artist = artistName
        mp3.album = albumTitle
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
    #print(tags)
    return


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
    print('    2. WAV')
    print('    3. Flac')
    print()
    choiceFormat = int(input('Choice : \n'))
    emptyPrint(2)
    if choiceFormat == 1:
        for music in musics:
            if music.lower().endswith('.wav'):
                print('Converting ' + music + ' to Mp3 format')
                wav_audio = AudioSegment.from_file(pathToMusicFolder + music, format="wav")
                wav_audio.export("test.mp3", format="mp3")
            if music.lower().endswith('.flac'):
                print('Converting ' + music + ' to Mp3 format')
        return
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

def menu():
    emptyPrint(2)
    print('MENU :')
    print()
    print('    1. Show files')
    print('    2. Remove metadata')
    print('    3. Remove album cover')
    print('    4. Change audio format')
    print('    5. Exit')
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
        sys.exit()
    menu()

menu()