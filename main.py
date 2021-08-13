import sys
import os
import uuid
import moviepy.editor
from argparse import ArgumentParser
import speech_recognition as sr
from pydub import AudioSegment


def parse_args():
    parser = ArgumentParser(description = 'Extract text from videos')
    parser.add_argument('file', help = 'Video file path')
    
    if len(sys.argv) != 2:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def extract_audio(filepath):
    video = moviepy.editor.VideoFileClip(filepath)
    audio = video.audio
    
    audio_filepath = str(uuid.uuid1()) + '.mp3'
    audio.write_audiofile(audio_filepath)
    return audio_filepath


def convert_mp3_to_wav(audio_filepath):
    sound = AudioSegment.from_mp3(audio_filepath)
    
    audio_filepath_wav = str(uuid.uuid1()) + '.wav'
    sound.export(audio_filepath_wav, format='wav')

    return audio_filepath_wav


def recognize_text(audio_filepath_wav):
    r = sr.Recognizer()
    
    with sr.AudioFile(audio_filepath_wav) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text


if __name__ == '__main__':
    arguments = parse_args()

    if not os.path.isfile(arguments.file):
        print(f'{arguments.file} not found')
    else:
        filepath = arguments.file
        audio_mp3 = extract_audio(filepath)
        audio_wav = convert_mp3_to_wav(audio_mp3)
        text = recognize_text(audio_wav)

        os.remove(audio_mp3)
        os.remove(audio_wav)
        print(text)
