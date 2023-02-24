import json
import requests

def main():
    url = 'http://localhost:8080/api/article'
    with open('article.json', encoding='utf-8') as fp:
        articles = json.load(fp)
        for article in articles:
            res = requests.post(url, json=article)
            print(res.json())

        # print(articles)


if __name__ == '__main__':
    main()
