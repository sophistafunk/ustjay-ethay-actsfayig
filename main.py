import logging
import os

import requests
from flask import Flask, send_file, Response, url_for
from bs4 import BeautifulSoup

app = Flask(__name__)

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


def get_fact():
    logging.info('getting fact')

    response = requests.get('http://unkno.com')

    soup = BeautifulSoup(response.content, 'html.parser')
    facts = soup.find_all('div', id='content')

    logging.info(facts[0].getText())

    return facts[0].getText()


def get_pig_latin(fact):
    logging.info('sending fact to pig latinzer')

    payload = {'input_text': fact}
    r = requests.post(
        'https://hidden-journey-62459.herokuapp.com/piglatinize/',
        data=payload,
        allow_redirects=False
    )

    logging.info(r.headers)

    return r.headers['Location']


@app.route('/')
def home():
    fact = get_fact().strip()
    body = get_pig_latin(fact)
    #body_url = url_for('get_pig_latin')
    return Response(response=body, mimetype='text/plain')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6787))
    app.run(host='0.0.0.0', port=port)

