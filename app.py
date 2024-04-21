from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline,AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

# Specify the model and revision explicitly
model_name = "sshleifer/distilbart-cnn-12-6"
revision = "a4f8f3e"

@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    transcript = get_transcript(video_id)
    if transcript:
        summary = get_summary(transcript)
        return summary, 200
    else:
        return "No subtitles found for the provided video URL.", 404

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

def get_summary(transcript):
    # Load the model and tokenizer
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, revision=revision)
    tokenizer = AutoTokenizer.from_pretrained(model_name, revision=revision)
    
    summariser = pipeline('summarization', model=model, tokenizer=tokenizer)
    summary = ''
    input_length = len(transcript)
    max_length = min(200, input_length)  # Adjust the maximum length dynamically
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summariser(transcript[i*1000:(i+1)*1000], max_length=max_length)[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary

if __name__ == '__main__':
    app.run()
