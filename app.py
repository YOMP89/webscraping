from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data['url']

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            alt_tags = [img.get('alt') for img in soup.find_all('img')]
            title_tags = [link.get('title') for link in soup.find_all('a')]

            return jsonify({
                'alt_tags': alt_tags,
                'title_tags': title_tags
            })
        else:
            return jsonify({'error': 'No se pudo acceder a la página'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
