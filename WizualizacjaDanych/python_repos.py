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
print("\nKlucze:", len(repo_dict))
for key in sorted(repo_dict.keys()):
    print(key)

# Przetworzenie wyników
print(response_dict.keys())