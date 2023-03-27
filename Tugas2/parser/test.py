import requests
from bs4 import BeautifulSoup

class Parsing:
    
    def __init__(self, url):
        self.url = url
        self.response = None
        self.container = None
        self.Bsoup = None
        
    def check(self):
        self.response = requests.get(self.url)
        self.container = self.response.content
        self.Bsoup = BeautifulSoup(self.container, 'html.parser')
        
    def start(self):
        list = self.Bsoup.find('ul',{'class': 'navbar-nav h-100 wdm-custom-menus links'})
        respond = []
        try:
            findLi = list.find_all('li')
            
            for menu in findLi:
                findA = menu.find('a')
                
                if findA:
                    respond.append(findA.text.strip())
                    findDiv = menu.find('div')
                    inside_a = findDiv.find_all('a')
                    for inside in inside_a:
                        respond.append('\t' + inside.text.strip())
                        
        except AttributeError:
            pass
        return respond
            
if __name__ == "__main__":
    html = Parsing('https://classroom.its.ac.id/')
    html.check()
    
    # print("Menu : ", html.start())
    for menu in html.start():
        print(menu)
