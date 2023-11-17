import requests
from bs4 import BeautifulSoup
from major import getPage, dynamicMaxLimit, getUrlsHandler

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
                        return (True, link_dept)

def dynamicMaxLimitHandler(departments):
    if departments[0] == False:
        return (False, [])
    else:
        depts = departments[1]
        dept_limit = []
        for d in depts:
            max_limit = dynamicMaxLimit(d[0])
            if max_limit[0] == False:
                return (False, [])
            dept_limit.append((d[0], max_limit[1]))
        return (True, dept_limit)

def departmentUrlHandler(deptinfo):
    if deptinfo[0] == False:
        return (False, [])
    else:
        baseUrl_maxLimit = deptinfo[1]
        dept_urls = []
        for BandM in baseUrl_maxLimit:
            dept_course_links = getUrlsHandler(BandM)
            if dept_course_links[0] == False:
                return (False, [])
            else:
                dept_urls.append(dept_course_links[1])
        return (True, dept_urls)
