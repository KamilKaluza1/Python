import requests
from operator import itemgetter

# Wykonanie wywołania API i zachowanie otrzymanej odpowiedzi.
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = requests.get(url)
print(f'Kod stanu: {r.status_code}')

# Przetworzenie informacji o każdym artykule.
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:30]:
    # Przygotowanie oddzielneg wywołania API dla każdego artykułu.
    url = ('https://hacker-news.firebaseio.com/v0/item/' + str(submission_id) + '.json')
    submission_r = requests.get(url)
    print(submission_r.status_code)
    response_dict = submission_r.json()

    submission_dict = {
        'title': response_dict['title'],
        'link': 'http://news.ycombinator.com/item?id=' + str(submission_id),
        'comments': response_dict.get('descendants', 0)
        }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

for submission_dict in submission_dicts:
    print(f'\n\nTytuł artykułu: {submission_dict["title"]}'
          f'\nŁącze do dyskusji: {submission_dict["link"]}'
          f'\nLiczba komentarzy: {submission_dict["comments"]}')
