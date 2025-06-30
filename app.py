from WebCrawler.models import Scraper
from flask import Flask, render_template, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config.from_pyfile('instance/config.py')


def scrape_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    links = soup.find_all('a')
    return links
@app.route("/", methods=["GET", "POST"])
def index():
    form = Scraper()
    links = None
    if form.validate_on_submit():
        links = scrape_links(form.url.data)
    return render_template('index.html', form=form, links=links)



if __name__ == "__main__":
    app()