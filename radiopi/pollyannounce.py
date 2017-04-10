import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import hashlib
import subprocess
import sys

# you will need to login with the AWS command line tool or add your credentials and use the second version of this line
polly = boto3.client('polly')
#polly = boto3.client('polly', aws_access_key_id="your access ID", aws_secret_access_key="your secret key", region_name="region, such as 'us-west-2'")


def play_speech(text):
    file_path = get_speech_file(text)

    if file_path is not None:
        subprocess.Popen(['mpg123', '-q', file_path]).wait()


def get_speech_file(text):
    file_path = get_speech_file_path(text)

    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        return file_path

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print("Error connecting to AWS:")
        print(error)
        return None

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important as the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            try:
                # Open a file for writing the output as a binary stream
                with open(file_path, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print("Error writing speech file:")
                print(error)
                return None

        return file_path
    else:
         # The response didn't contain audio data, exit gracefully
        print("Response did not contain 'AudioStream'")
        return None


def get_speech_file_path(text):
    DIRECTORY = 'speeches'
    FILENAME = '{hash}.mp3'

    speech_dir_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], DIRECTORY)

    if not os.path.exists(speech_dir_path):
        os.makedirs(speech_dir_path)

    hash = hashlib.md5(text).hexdigest()
    filename_with_path = os.path.join(speech_dir_path, FILENAME.format(hash=hash))

    return filename_with_path
