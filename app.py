from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

app = Flask(__name__)

@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    summary = get_summary(get_transcript(video_id))
    return summary, 200

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

def get_summary(transcript):
    summariser = pipeline('summarization')
    summary = ''
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary 

# # Specify the exact model and revision
# model_name = "sshleifer/distilbart-cnn-12-6"
# revision = "a4f8f3e"
# summarizer = pipeline("summarization", model=model_name, revision=revision)

# # Adjust the max_length parameter
# max_length = 50  # You can adjust this value based on your requirements

# # Assuming you have a function to fetch the URL content
# def fetch_url_content(url):
#     # Code to fetch URL content goes here
#     pass

# # Example usage
# url = "https://www.youtube.com/watch?v=zkczDkbaE68"
# content = fetch_url_content(url)
# summary = summarizer(content, max_length=max_length)

# print(summary)


if __name__ == '__main__':
    app.run()
