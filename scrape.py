import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="",
#   database="itlexp7"

# )

# print(mydb)

result = requests.get("https://it.spit.ac.in/faculty/")

print(result.status_code)

# print(result.headers)

src = result.content

# print(src)

soup = BeautifulSoup(src,'html.parser')

#print(soup.find_all('a'))
data = []
table = soup.find('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])
# print(data)

name = list()
branch = list()
for this_name, this_branch in data:
    name.append(this_name)
    branch.append(this_branch)
# print(name)
# print(branch)

df = pd.DataFrame(list(zip(name, branch)),
               columns =['Name', 'Branch'])

# print(df.head())

data_internal = []
table = soup.find('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')
links = []
anchor = []
for tr in rows:
    cols = tr.find_all('td')
    for a in cols:
        anchor.append(a.find_all('a'))

for m in anchor:
    if len(m) != 0:
        # print(m[0]['href'])
        links.append(m[0]['href'])

# print(links)

links_final = []

for element in links:
    element = "https://it.spit.ac.in" + element
    # print(element)
    links_final.append(element)


# print(links_final)

data_new = []

for link in links_final:
    results = requests.get(str(link))
    src = results.content
    soup = BeautifulSoup(src,'html.parser')
    p = soup.find_all('p')
    for text in p:
        if '{at}' in text.get_text():
            # print (text.get_text())
            data_new.append(text.get_text())
print(data_new)









# li_tag = soup.find_all('li',class_="content-slider__item")

# title_of_player = []

# for a in li_tag:
#     head = a.find('div',class_="leaderHeader").get_text()
#     title_of_player.append(head.strip())
    
# stat_tag = soup.find_all('div',class_="stat-content")

# names = []
# for b in stat_tag:
#     name = b.find('h1').get_text()
#     names.append(name.strip())

# stats_cont = soup.find_all('div',class_="stat-container")

# stats_val1 = []

# for c in stats_cont:
#     val1 = c.find('span',class_="digits").get_text()
#     val2 = c.find('span',class_="statLabel").get_text()
#     stats_val1.append(val1.strip() + " " + val2.strip())

# print(stats_val1)
# print(names)
# print(title_of_player)

# mycursor = mydb.cursor()

# for d in range(0,10):
#     sql = "INSERT INTO stats (name, record, value) VALUES (%s,%s,%s)"
#     val = (names[d],title_of_player[d],stats_val1[d])
#     mycursor.execute(sql, val)
#     mydb.commit()
#     print(mycursor.rowcount, "record inserted.")

df = pd.DataFrame(list(zip(name, branch, data_new)),
               columns =['Name', 'Branch', ' Data'])

print(df.head())

df.to_excel("spit_it.xlsx")