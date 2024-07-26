import os
import ctypes
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError, error
from mutagen.mp3 import MP3

os.system('cls')

def convert(num):

    #Tao UID dua vao tracknumber cua file

    #Args:
    #   num (int): tracknumber cua file

    #Returns:
    #   UID (str): UID cua file

    UID = str(num)
    while len(UID)-9:
        UID = '0'+UID
    
    return UID

def main():

    path = os.path.abspath(__file__)

    # directory chua duong dan den CWD
    directory = os.path.dirname(path)
    
    # folder la list chua cac ten folder co trong CWD
    folder = []

    # luu ten cac file luu vao folder
    for filename in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, filename)):
            folder.append(filename)

    
    # Thoat CT neu khong co folder nao
    if len(folder) == 0:
        input('No folder found!')
        exit()

    for playlist in folder:

        with open('lastest_UID_generated.txt', 'r') as UID_gen:
            # lastest_UID la gia tri UID moi nhat luu trong file lastest_UID_generated.txt
            lastest_UID = int(UID_gen.readline())            
            UID_gen.close()
            
        playlist_path = directory + '\\' +playlist
        
        # Chua ten file va bo qua cac file co chua tu 'Album' va 'Folder'
        music_list = [music for music in os.listdir(playlist_path) if 'Album' \
                      not in music and 'Folder' not in music]

        # track_num chua gia tri tong so file co trong tung playlist
        track_num = len(music_list)
        

        print('Currently in ', playlist)
            
        for music_name in music_list:
         
            music_path = playlist_path + '\\' + music_name
            try:
                #khai bao bien music metadata don gian
                music = MP3(music_path, ID3 = EasyID3) 
                title = music['title'][0];
                tracknumber = music['tracknumber'][0]
                music.save()

                #Tao UID bang lastestUID + so thu tu cua file trong playlist
                UID = convert(lastest_UID + int(tracknumber))

                # Gan UID vao ten file
                os.rename(music_path, playlist_path + '\\' + UID + '_' + title + '.mp3')
                
                print('\t', title, ' is saved with UID ',UID)

            # Phat hien loi ten file
            except error as e:
                print('\tError occured when trying to edit the file ', music_name)

            # Phat hien loi file hong
            except ID3NoHeaderError:
                print('\tError occured when trying to edit the file ', music_name)

            # Phat hien cac loi khac
            except Exception as e:
                print('\tError occured when trying to edit the file ', music_name)

        #Luu lai lastest_UID moi vao file lastest_UID_generated.txt      
        with open('lastest_UID_generated.txt', 'w') as UID_gen:
            UID_gen.write(convert(lastest_UID + track_num))
            UID_gen.close()

        print('\n')

main()    
input('Run successfully, now fck off!')  

    
