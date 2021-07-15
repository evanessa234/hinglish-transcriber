from __future__ import unicode_literals
from flask import Flask, request, render_template, redirect, url_for
import youtube_dl

app = Flask(__name__)

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': './static/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        # 'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

@app.route("/", methods = ["GET", "POST"])
def hello_world():
    # return "<p>Hello, World!</p>"
    return render_template("index.html")
    
@app.route("/linking", methods = ["GET", "POST"])
def link_to_mp3():
    video_link = str(request.form["video_link"])
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])
    return render_template("temp.html", video_link=video_link)



if __name__ == "__main__":
    app.run(debug=True)
