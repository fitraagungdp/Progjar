import requests
from bs4 import BeautifulSoup

class HTMLParser:
    def __init__(self, url):
        self.url = url
        self.response = None
        self.html_content = None
        self.soup = None
        
    def get(self):
        self.response = requests.get(self.url)
        self.html_content = self.response.content
        self.soup = BeautifulSoup(self.html_content, 'html.parser')
     
    def get_menu(self):
        menu_list = self.soup.find(
            'ul', {'class': 'navbar-nav h-100 wdm-custom-menus links'})
        res = []
        try:
            li_menus = menu_list.find_all('li')
            for menu in li_menus:
                a = menu.find('a')
                if a:
                    res.append(a.text.strip())
                    div = menu.find('div')
                    inside_a = div.find_all('a')
                    for inside in inside_a:
                        res.append('\t' + inside.text.strip())
        
        except AttributeError:
            pass
        return res
    
if __name__ == "__main__":
    html = HTMLParser('https://classroom.its.ac.id/')
    html.get()
    
    print("Menu : ", html.get_menu())
    for menu in html.get_menu():
        print(menu)