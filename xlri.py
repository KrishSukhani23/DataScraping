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

result = requests.get("https://www.xlri.ac.in/faculty-research/faculty-members.aspx")

print(result.status_code)

# print(result.headers)

src = result.content

# print(src)

soup = BeautifulSoup(src,'html.parser')
data = []
main_data = soup.find_all(class_ = "hide" )
for a in main_data:
    # print(a.find_all("a",class_  ="report"))
    for m in a.find_all("a",class_  ="report"):
        data.append(m.get_text())


links = []

main_data_new = soup.find_all(class_ = "hide" )
for a in main_data_new:
    # print(a.find_all("a",class_  ="report"))
    for m in a.find_all("a",class_  ="report"):
        links.append(m['href'])
# print(links)

links_final = []

for element in links:
    element = "https://www.xlri.ac.in/faculty-research/" + element
    # print(element)
    links_final.append(element)
# print(links_final)



degree = []
academic_area = []
email = []

for link in links_final:
    results = requests.get(str(link))
    src = results.content
    soup = BeautifulSoup(src,'html.parser')
    degree.append(soup.find(id="lblDegree").get_text())
    academic_area.append(soup.find(id="lblAcademicArea").get_text())
    email.append(soup.find(id="lblFacultyEmail").get_text())
    
print(degree)
print(academic_area)
print(email)    
    # p = soup.find_all('p')
    # for text in p:
    #     if '{at}' in text.get_text():
    #         # print (text.get_text())
    #         data_new.append(text.get_text())
# print(data_new)

df = pd.DataFrame(list(zip(data, degree, academic_area, email, links_final)),
               columns =['Name', 'Degree', 'Academic Area', 'Email', 'Link'])

print(df.head())

df.to_excel("xlri.xlsx")


# data.to_excel("xlri.xlsx")