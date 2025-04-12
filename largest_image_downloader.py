import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import unquote

def get_largest_image_url(img_url, base_url):
    """Находит URL изображения в максимальном разрешении."""
    # Удаляем параметры размера (например, -300x200.jpg)
    clean_url = re.sub(r'-\d+x\d+(?=\.\w+$)', '', img_url)
    if clean_url != img_url:
        return clean_url
    return img_url

def download_images(url, save_folder='images'):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        img_tags = soup.find_all('img')
        print(f"Найдено изображений: {len(img_tags)}")
        
        downloaded_urls = set()  # Чтобы избежать дубликатов
        
        for i, img in enumerate(img_tags, 1):
            # Ищем URL в разных атрибутах
            img_url = (img.get('src') or 
                      img.get('data-src') or 
                      img.get('data-large') or 
                      img.get('data-full-url'))
            
            if not img_url:
                continue
            
            # Преобразуем относительный URL в абсолютный
            img_url = urljoin(url, unquote(img_url))
            
            # Получаем URL изображения в максимальном разрешении
            largest_url = get_largest_image_url(img_url, url)
            
            if largest_url in downloaded_urls:
                print(f"[{i}] Пропущено (дубликат): {os.path.basename(largest_url)}")
                continue
            
            try:
                # Проверяем, существует ли файл
                filename = os.path.basename(largest_url.split('?')[0])
                if not filename:
                    filename = f"image_{i}.jpg"
                
                filepath = os.path.join(save_folder, filename)
                
                if os.path.exists(filepath):
                    print(f"[{i}] Файл уже существует: {filename}")
                    continue
                
                # Загружаем изображение
                img_data = requests.get(largest_url, headers=headers, stream=True)
                img_data.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    for chunk in img_data.iter_content(1024):
                        f.write(chunk)
                
                downloaded_urls.add(largest_url)
                print(f"[{i}] Сохранено: {filename} (размер: {os.path.getsize(filepath) // 1024} KB)")
            
            except Exception as e:
                print(f"[{i}] Ошибка загрузки {largest_url}: {e}")
    
    except Exception as e:
        print(f"Ошибка при обработке страницы: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Скачивает изображения в максимальном разрешении')
    parser.add_argument('url', help='URL страницы для парсинга изображений')
    parser.add_argument('--folder', default='images', help='Папка для сохранения (по умолчанию: images)')
    
    args = parser.parse_args()
    
    print(f"\nЗагрузка изображений с: {args.url}")
    print(f"Папка для сохранения: {args.folder}\n")
    
    download_images(args.url, args.folder)