import os

from WebCrawler.models import Link
from static.db import db
from flask import Flask, render_template, redirect, url_for
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session

# deletes the db before re creating because i'm lazy
if os.path.exists("instance/webscraper.db"):
    os.remove("instance/webscraper.db")

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///webscraper.db"
app.config.from_pyfile('instance/config.py')

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()

# function that scrapes all links from set page
def scrape_links(url):
    print(f"I'm currently scraping {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    links = soup.find_all('a')
    return links



@app.route("/", methods=["GET", "POST"])
def index():


    # initially adding the starting url to the database
    starting_link = Link(
        url="https://URL-GOES-HERE/")
    db.session.add(starting_link)
    db.session.commit()
    id = 0

    while True:
        domain = "https://URL-GOES-HERE"
        # set a variable that checks if link id is greater than the id variable
        url = db.session.query(Link).filter(Link.id > id).first()
        # if it gets to the bottom of the database it breaks the loop
        if not url:
            break

        # this is what jumps to the next page and scrapes from that page
        links = scrape_links(url.url)

        for link in links:
            # filters the href from the a tag in html
            href = link.get('href')
            if href:
                # fun little bug finder :3
                if href != href.strip():
                    print(f"Found link with space '{href}' on {url.url}")
                href = href.strip()
                # filter out some of the reasons why the code exploded
                if href[0] == "#":
                    continue
                if href.startswith("tel:"):
                    continue
                if href.startswith("javascript:"):
                    continue
                if href.startswith("mailto:"):
                    continue
                if href.endswith(".pdf") or href.endswith(".m4a") or href.endswith(".mp3"):
                    continue
                # this is for the links that are shortened, adds the domain to it
                if not href.startswith("http://") and not href.startswith("https://"):
                    if "://" in href:
                        continue
                    href = domain + href
                if not href.startswith("http://URL-GOES-HERE") and not href.startswith("https://URL-GOES-HERE"):
                    continue
                # if the href is unique add to the database
                if not db.session.query(Link).filter_by(url=href).first():
                    new_link = Link(url=href)
                    db.session.add(new_link)
        id = url.id
        db.session.commit()

    return render_template('index.html', domain=domain, links=links, db_links=db_links)



if __name__ == "__main__":
    app()