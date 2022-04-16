import requests

# Wykonanie wywołania API i zachowanie otrzymanej odpowiedzi.
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
r = requests.get(url)
print("Kod stanu:", r.status_code)
# Umieszczenie odpowiedzi API w zmiennej.
response_dict = r.json()
print("Całkowita liczba repozytoriów:", response_dict['total_count'])

# Przetworzenie informacji o repozytoriach.
repo_dicts = response_dict['items']
print("Liczba zwróconych repozytoriów:", len(repo_dicts))
# Przeanalizowanie pierwszego repozytorium.
repo_dict = repo_dicts[0]

print(f'\nWybrane informacje o pierwszym repozytorium:')
for repo_dict in repo_dicts:
    print(f'Nazwa: {repo_dict["name"]}\n'
          f'Właściciel: {repo_dict["owner"]["login"]}\n'
          f'Gwiazdki: {repo_dict["stargazers_count"]}\n'
          f'Repozytorium: {repo_dict["html_url"]}\n'
          f'Utworzone: {repo_dict["created_at"]}\n'
          f'Uaktualnione: {repo_dict["updated_at"]}\n'
          f'Opis: {repo_dict["description"]}\n')
