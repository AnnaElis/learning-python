import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urlparse

def check_broken_links(start_url, max_pages=50):
    """Проверяет сайт на битые ссылки."""
    domain = urlparse(start_url).netloc  # Извлекаем домен
    visited = set()
    broken_links = []
    to_visit = {start_url}

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop()
        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=10)
            visited.add(url)
            print(f"Проверено: {url} ({len(visited)}/{max_pages})")

            if response.status_code == 404:
                broken_links.append(url)
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('http') and domain in href:
                        to_visit.add(href)
            
            time.sleep(0.5)  # Защита от блокировки

        except Exception as e:
            print(f"Ошибка при проверке {url}: {str(e)}")
            broken_links.append(url)

    return broken_links

def main():
    print("=== Проверка битых ссылок на сайте ===")
    site_url = input("Введите URL сайта (например, https://vitoslavica.ru): ").strip()
    
    if not site_url.startswith(('http://', 'https://')):
        site_url = 'https://' + site_url  # Добавляем схему по умолчанию

    print(f"\n🔍 Начинаю проверку: {site_url}")
    broken_links = check_broken_links(site_url, max_pages=2000)  # Уменьшено для теста

    # Генерируем имя файла на основе домена
    domain = urlparse(site_url).netloc.replace('.', '_')
    report_filename = f"broken_links_{domain}.csv"
    
    # Сохраняем отчет
    pd.DataFrame(broken_links, columns=["Битые ссылки"]).to_csv(report_filename, index=False)
    print(f"\n✅ Отчет сохранен в файл: {report_filename}")
    print(f"Найдено битых ссылок: {len(broken_links)}")

if __name__ == "__main__":
    main()
