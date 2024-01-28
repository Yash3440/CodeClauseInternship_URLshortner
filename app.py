from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import shortuuid
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class ShortenedURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_id = db.Column(db.String(8), unique=True, nullable=False)
    original_url = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, original_url):
        self.original_url = original_url
        self.short_id = shortuuid.uuid()[:8]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_url = ShortenedURL(original_url=original_url)
        db.session.add(short_url)
        db.session.commit()
        return redirect('/')
    urls = ShortenedURL.query.all()
    return render_template('index.html', urls=urls)

@app.route('/<short_id>')
def short_url(short_id):
    url = ShortenedURL.query.filter_by(short_id=short_id).first_or_404()
    return redirect(url.original_url)

if __name__ == '__main__':
    app.run(debug=True)
