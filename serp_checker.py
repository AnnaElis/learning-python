import requests
from bs4 import BeautifulSoup
import time
import csv
from urllib.parse import quote_plus

class SERPChecker:
    def __init__(self, site_url):
        self.site_url = site_url
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        
    def check_google(self, keyword, pages=3):
        positions = []
        for page in range(pages):
            start = page * 10
            url = f"https://www.google.com/search?q={quote_plus(keyword)}&start={start}"
            
            headers = {"User-Agent": self.user_agent}
            try:
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    results = soup.find_all('div', class_='g')
                    
                    for i, result in enumerate(results[:10], start=1):
                        link = result.find('a')['href'] if result.find('a') else None
                        if link and self.site_url in link:
                            positions.append(page * 10 + i)
            except Exception as e:
                print(f"Ошибка при проверке Google: {e}")
            
            time.sleep(2)
            
        return positions if positions else None
    
    def check_yandex(self, keyword, pages=3):
        positions = []
        for page in range(pages):
            url = f"https://yandex.ru/search/?text={quote_plus(keyword)}&p={page}"
            
            headers = {"User-Agent": self.user_agent}
            try:
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    results = soup.find_all('li', class_='serp-item')
                    
                    for i, result in enumerate(results[:10], start=1):
                        link = result.find('a', class_='organic__url')['href'] if result.find('a', class_='organic__url') else None
                        if link and self.site_url in link:
                            positions.append(page * 10 + i)
            except Exception as e:
                print(f"Ошибка при проверке Яндекс: {e}")
            
            time.sleep(2)
            
        return positions if positions else None
    
    def run_check(self, keywords):
        results = []
        
        for keyword in keywords:
            print(f"Проверяю ключевое слово: {keyword}")
            
            google_pos = self.check_google(keyword)
            yandex_pos = self.check_yandex(keyword)
            
            results.append({
                'keyword': keyword,
                'google': google_pos,
                'yandex': yandex_pos
            })
        
        return results
    
    def save_to_csv(self, results, filename='serp_results.csv'):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['keyword', 'google', 'yandex'])
            writer.writeheader()
            writer.writerows(results)
        print(f"Результаты сохранены в файл: {filename}")

def get_keywords_from_input():
    print("Введите ключевые слова для проверки (каждое с новой строки). Для завершения ввода введите пустую строку:")
    keywords = []
    while True:
        keyword = input().strip()
        if not keyword:
            break
        keywords.append(keyword)
    return keywords

if __name__ == "__main__":
    print("=== SERP Position Checker ===")
    site_url = input("Введите URL вашего сайта (например, vitoslavica.ru): ").strip()
    
    # Получаем ключевые слова от пользователя
    keywords = get_keywords_from_input()
    
    if not keywords:
        print("Не введено ни одного ключевого слова. Выход.")
        exit()
    
    checker = SERPChecker(site_url)
    results = checker.run_check(keywords)
    checker.save_to_csv(results)
    
    print("\nРезультаты проверки:")
    for result in results:
        print(f"\nКлючевое слово: {result['keyword']}")
        print(f"Позиции в Google: {result['google'] or 'Не найдено'}")
        print(f"Позиции в Яндекс: {result['yandex'] or 'Не найдено'}")
    
    print("\nПроверка завершена!")