app.py
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    arquivos = []
    url = ""
    if request.method == 'POST':
        url = request.form['url']
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')

            for link in links:
                href = link.get('href')
                if href and (href.endswith('.pdf') or href.endswith('.docx') or href.endswith('.txt')):
                    if href.startswith('http'):
                        arquivos.append(href)
                    else:
                        arquivos.append(url.rstrip('/') + '/' + href.lstrip('/'))
        except Exception as e:
            arquivos = [f"Erro: {e}"]

    return render_template('index.html', arquivos=arquivos, url=url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
