import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse  # Для обработки аргументов командной строки

def download_images(url, save_folder='images'):
    # Создаем папку для сохранения, если её нет
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    # Заголовки, чтобы сайты не блокировали запрос
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Получаем HTML-код страницы
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверяем, не вернулась ли ошибка HTTP
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Находим все теги img, а также изображения внутри data-src (ленивая загрузка)
        img_tags = soup.find_all('img')
        
        print(f"Найдено изображений: {len(img_tags)}")
        
        for i, img in enumerate(img_tags, 1):
            # Получаем URL изображения (проверяем src, data-src и другие атрибуты)
            img_url = img.get('src') or img.get('data-src') or img.get('data-lazy')
            if not img_url:
                continue
            
            # Собираем абсолютный URL, если он относительный
            img_url = urljoin(url, img_url)
            
            try:
                # Получаем содержимое изображения
                img_data = requests.get(img_url, headers=headers, stream=True).content
                
                # Извлекаем имя файла из URL
                filename = os.path.basename(img_url).split('?')[0]  # Удаляем параметры запроса
                if not filename:
                    filename = f"image_{i}.jpg"  # Если имя не извлечено, создаем свое
                
                # Сохраняем в папку
                filepath = os.path.join(save_folder, filename)
                
                # Проверяем, не существует ли файл
                if os.path.exists(filepath):
                    print(f"Файл уже существует: {filename}")
                    continue
                
                # Записываем изображение
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                
                print(f"[{i}] Сохранено: {filename}")
            
            except Exception as e:
                print(f"Ошибка при загрузке {img_url}: {e}")
    
    except Exception as e:
        print(f"Ошибка при обработке страницы: {e}")

if __name__ == "__main__":
    # Настраиваем аргументы командной строки
    parser = argparse.ArgumentParser(description='Скачивает все изображения с веб-страницы')
    parser.add_argument('url', help='URL страницы для парсинга изображений')
    parser.add_argument('--folder', default='images', help='Папка для сохранения (по умолчанию: images)')
    
    args = parser.parse_args()
    
    print(f"\nЗагрузка изображений с: {args.url}")
    print(f"Сохранение в папку: {args.folder}\n")
    
    download_images(args.url, args.folder)
