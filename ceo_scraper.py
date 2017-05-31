from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
import re, csv, sys, os.path

# ============================================
# setup
Ceos = []
class Ceo(object):
    def __init__(self, name = "none", company = "none", id = 0):
        self.name = name
        self.company = company
        self.id = id
    
    def get_name(self):
        return self.name

    def get_company(self):
        return self.company

    def get_id(self):
        return self.id

f = open("sp1500ceo_2015.csv")
csv_f = csv.reader(f)
for row in csv_f:
    if row[0]!="obs":
        Ceos.append(Ceo(row[5],row[3],row[0]))

# ============================================
# create html
print("Creating HTML\n")

for x in tqdm(Ceos):
    if False: #os.path.isfile("html_files/{}.html".format(x.get_id())):
        pass
    else:
        link = "https://www.google.com/search?as_st=y&tbm=isch&hl=en&as_q={}+{}&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=itp:face,ic:color".format(x.get_name(),x.get_company())

        driver = webdriver.PhantomJS()
        driver.set_window_size(1120, 550)
    
        driver.get(link)
        td = driver.find_elements_by_css_selector('[style="width:25%;word-wrap:break-word"]')

        with open("html_files/{}.html".format(x.get_id()), "w") as g:
            g.write(driver.page_source)

# ============================================
# extract images
print("Extracting Images\n")

for x in tqdm(Ceos):
    html = "html_files/{}.html".format(x.get_id())
    count = 0
    
    with open(html) as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    links = [td.a.img for td in soup.findAll("td", style = "width:25%;word-wrap:break-word")]
    for link in links:
        #subprocess.call(["wget", link.get("src"), "-O", "image_files/" + x.get_id() + ".png"])
        subprocess.call(["wget", link.get("src"), "-O", x.get_id() + ".jpeg"])
        break

