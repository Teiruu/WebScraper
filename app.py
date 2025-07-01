from WebCrawler.models import Scraper, Link, Base
from flask import Flask, render_template, redirect, url_for
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# create engine and session
engine = create_engine('sqlite:///links.db')
Session = sessionmaker(bind=engine)
session = Session()
app = Flask(__name__)
app.config.from_pyfile('instance/config.py')

# create the table
Base.metadata.create_all(engine)

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
        for link in links:
            href = link.get('href')
            if href:  # only save valid hrefs
                if not session.query(Link).filter_by(url=href).first():
                    new_link = Link(url=href)
                    session.add(new_link)
        session.commit()
    return render_template('index.html', form=form, links=links)



if __name__ == "__main__":
    app()