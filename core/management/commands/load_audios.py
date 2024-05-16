import os
import glob
from django.core.management import BaseCommand
from django.core.files import File
from core.models import AudioFiles

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('audio_path', type=str)

    def handle(self, *args, **options):
        audio_path = options["audio_path"]

        for folder in glob.glob(os.path.join(audio_path, "*")):
            print(folder)
            folder_name = os.path.basename(folder)
            block_num = int(folder_name.replace("block", ""))
            nnn = 0
            for file in sorted(glob.glob(os.path.join(folder, "*.mp3"))):
                print(file)
                file_name = os.path.basename(file)
                audio = AudioFiles()
                audio.name = file_name
                audio.active = True
                audio.block = block_num
                nnn += 1
                audio.number = nnn
                with open(file, 'rb') as ff:
                    audio.file.save(file_name, File(ff), save=True)
                    # print(ff)
                    # content = ff.read()
                audio.save()
        """
        for file in glob.glob(os.path.join(audio_path, "*.mp3")):
            print(file)
            file_name = os.path.basename(file)
            audio = AudioFiles()
            audio.name = file_name
            audio.active = True
            with open(file, 'rb') as ff:
                audio.file.save(file_name, File(ff), save=True)
                #print(ff)
                #content = ff.read()
            audio.save()
            #audio.file.save(file_name, content)
        """