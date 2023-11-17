import requests
from bs4 import BeautifulSoup
from major import getPage, dynamicMaxLimit

url = getPage('https://www.bu.edu/academics/com/courses/')

def getDepartment(url):
    data = url
    if data[0] == False:
        return (False, [])
    else:
        soup = BeautifulSoup(data[1], 'html.parser')
        course_filter_div = soup.find('div', class_='course-filter')
        if course_filter_div:
            first_ul = course_filter_div.find('ul')
            if first_ul:
                li = first_ul.find('li')
                if li:
                    ul = li.find('ul')
                    if ul:
                        link_dept = []
                        li_elements = ul.find_all('li')
                        for li in li_elements:
                            a_tag = li.find('a') 
                            if a_tag and a_tag.has_attr('href'):
                                text = a_tag.get_text(strip=True) 
                                if text == "All Departments": 
                                    continue
                                link = a_tag['href']
                                link_dept.append((link, text))
                        return link_dept

#departments = getDepartment(url)
#deptlimit = dynamicMaxLimit(departments[2][0])
#print(deptlimit)