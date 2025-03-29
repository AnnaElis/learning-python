import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse
import time
import json

class AdvancedSEOAnalyzer:
    def __init__(self, max_pages=50, delay=1.0):
        self.max_pages = max_pages
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})

    def is_valid_url(self, url, domain):
        """Проверяет, является ли URL допустимым для анализа"""
        parsed = urlparse(url)
        return (
            parsed.scheme in ('http', 'https') and
            parsed.netloc == domain and
            not parsed.fragment and
            not url.endswith(('.pdf', '.jpg', '.png', '.zip'))
        )

    def analyze_images(self, soup, base_url):
        """Анализирует изображения на странице"""
        images = []
        for img in soup.find_all('img'):
            img_data = {
                'src': urljoin(base_url, img.get('src', '')),
                'alt': img.get('alt', '❌ Отсутствует'),
                'width': img.get('width', 'Не указано'),
                'height': img.get('height', 'Не указано'),
                'loading': img.get('loading', 'Не указано (рекомендуется lazy)')
            }
            images.append(img_data)
        return images

    def analyze_microdata(self, soup):
        """Анализирует микроразметку (Schema.org, OpenGraph)"""
        microdata = {
            'schema': [],
            'og': {},
            'twitter': {}
        }

        # Schema.org
        for item in soup.find_all(attrs={'itemscope': True}):
            schema_type = item.get('itemtype', 'Не указан')
            microdata['schema'].append(schema_type)

        # OpenGraph
        for meta in soup.find_all('meta', attrs={'property': True}):
            if meta['property'].startswith('og:'):
                microdata['og'][meta['property']] = meta.get('content', '')

        # Twitter Cards
        for meta in soup.find_all('meta', attrs={'name': True}):
            if meta['name'].startswith('twitter:'):
                microdata['twitter'][meta['name']] = meta.get('content', '')

        return microdata

    def analyze_page(self, url, domain):
        """Полный анализ одной страницы"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Базовые мета-данные
            title = soup.title.string if soup.title else "❌ Отсутствует"
            meta_desc = (soup.find('meta', attrs={'name': 'description'})['content'] 
                        if soup.find('meta', attrs={'name': 'description'}) else "❌ Отсутствует")

            # Анализ заголовков
            headings = {f'h{i}': [h.get_text(strip=True) for h in soup.find_all(f'h{i}')] for i in range(1, 4)}

            # Анализ изображений
            images = self.analyze_images(soup, url)
            img_errors = sum(1 for img in images if img['alt'] == '❌ Отсутствует')

            # Анализ микроразметки
            microdata = self.analyze_microdata(soup)

            return {
                'URL': url,
                'Title': title,
                'Title_Length': len(title),
                'Meta_Description': meta_desc,
                'Meta_Length': len(meta_desc),
                'H1_Count': len(headings['h1']),
                'H2_Count': len(headings['h2']),
                'H3_Count': len(headings['h3']),
                'Images_Total': len(images),
                'Images_Without_Alt': img_errors,
                'Schema_Types': ', '.join(microdata['schema']) if microdata['schema'] else '❌ Отсутствует',
                'OG_Tags': len(microdata['og']),
                'Twitter_Tags': len(microdata['twitter']),
                'Status': response.status_code,
                'Domain': domain
            }
        except Exception as e:
            print(f"Ошибка при анализе {url}: {str(e)}")
            return None

    def crawl_site(self, start_url):
        """Рекурсивный обход сайта"""
        domain = urlparse(start_url).netloc
        visited = set()
        results = []
        
        to_visit = {start_url}
        while to_visit and len(visited) < self.max_pages:
            url = to_visit.pop()
            
            if url in visited:
                continue
                
            print(f"Анализирую: {url}")
            page_data = self.analyze_page(url, domain)
            if page_data:
                results.append(page_data)
            visited.add(url)
            time.sleep(self.delay)
            
            try:
                response = self.session.get(url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    
                    if (self.is_valid_url(full_url, domain) 
                        and full_url not in visited 
                        and len(visited) < self.max_pages):
                        to_visit.add(full_url)
                        
            except Exception as e:
                print(f"Ошибка при обработке ссылок на {url}: {str(e)}")
        
        return results

def main():
    print("=== Продвинутый SEO-анализатор ===")
    print("Введите URL сайтов через запятую (например: site1.ru, site2.com)")
    user_input = input("URL сайтов: ").strip()
    
    urls = [url.strip() for url in user_input.split(',') if url.strip()]
    
    analyzer = AdvancedSEOAnalyzer(max_pages=50, delay=1.0)
    all_results = []
    
    for url in urls:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        print(f"\n🔍 Начинаю анализ сайта: {url}")
        site_results = analyzer.crawl_site(url)
        all_results.extend(site_results)
    
    if all_results:
        df = pd.DataFrame(all_results)
        
        # Добавляем рекомендации
        df['Title_Recommendation'] = df['Title_Length'].apply(
            lambda x: "✅ OK" if 50 <= x <= 60 else "⚠️ Слишком короткий" if x < 50 else "⚠️ Слишком длинный")
        
        df['Meta_Recommendation'] = df['Meta_Length'].apply(
            lambda x: "✅ OK" if 120 <= x <= 160 else "⚠️ Слишком короткое" if x < 120 else "⚠️ Слишком длинное")
        
        df['Images_Recommendation'] = df.apply(
            lambda x: "✅ OK" if x['Images_Without_Alt'] == 0 
            else f"⚠️ {x['Images_Without_Alt']} без alt", axis=1)
        
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M')
        filename = f"advanced_seo_report_{timestamp}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\n📊 Отчет сохранен в файл: {filename}")
        print("\nСводная статистика по сайтам:")
        print(df.groupby('Domain').agg({
            'H1_Count': 'mean',
            'Images_Without_Alt': 'sum',
            'OG_Tags': 'mean',
            'Schema_Types': lambda x: (x != '❌ Отсутствует').mean()
        }).round(2))
        
        # Сохраняем примеры микроразметки
        sample_microdata = {}
        for _, row in df[df['OG_Tags'] > 0].head(2).iterrows():
            sample_microdata[row['URL']] = {
                'OG': json.loads(row.to_json())['OG_Tags'],
                'Schema': row['Schema_Types']
            }
        
        with open(f"microdata_samples_{timestamp}.json", 'w') as f:
            json.dump(sample_microdata, f, indent=2)
        print(f"\nПримеры микроразметки сохранены в microdata_samples_{timestamp}.json")
        
    else:
        print("❌ Не удалось получить данные для анализа")

if __name__ == "__main__":
    main()
