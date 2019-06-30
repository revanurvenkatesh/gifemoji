from __future__ import print_function
import time
import boto3
import json

client = boto3.client('s3')

def upload_to_bucket(filename):
    client.upload_file(filename, 'meme-audio', filename)

def read_transcribe_output(job_name):
    obj = client.get_object(Bucket='transcribe-output-meme', Key=job_name + ".json")
    json_string = obj['Body'].read().decode('utf-8')
    output_json = json.loads(json_string)
    transcript = output_json['results']['transcripts'][0]['transcript']
    return transcript

def transcribe_job(file_name):
    transcribe = boto3.client('transcribe')
    transcribe.start_transcription_job(
    TranscriptionJobName=file_name,
    Media={'MediaFileUri': "s3://meme-audio/" + file_name},
    MediaFormat='wav',
    LanguageCode='en-US',
    OutputBucketName='transcribe-output-meme'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=file_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    transcript = read_transcribe_output(file_name)
    return transcript

file_name = 'taylor.wav'
upload_to_bucket(file_name)
transcript = transcribe_job(file_name)
print(transcript)