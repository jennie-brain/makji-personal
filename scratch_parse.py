import bs4
import re

file_path = r'C:\Users\Administrator\workspace\makji\prototypes\거의최종프로토타입.html'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = bs4.BeautifulSoup(f, 'html.parser')
        
    print('--- Document Structure ---')
    for tag in soup.find_all(['header', 'nav', 'main', 'section', 'footer', 'article']):
        tag_id = tag.get('id', '')
        tag_class = ' '.join(tag.get('class', []) if isinstance(tag.get('class'), list) else [tag.get('class', '')])
        print(f'<{tag.name} id=\"{tag_id}\" class=\"{tag_class}\">')
        
    print('\n--- Scripts ---')
    for script in soup.find_all('script'):
        src = script.get('src')
        if src:
            print(f'External Script: {src}')
        elif script.string:
            snippet = script.string.strip()[:100].replace('\n', ' ')
            print(f'Inline Script snippet: {snippet}...')
            
except Exception as e:
    print(f'Error: {e}')
