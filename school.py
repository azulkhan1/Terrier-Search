import requests
from bs4 import BeautifulSoup
from major import getPage, dynamicMaxLimit, getUrlsHandler, getCourseContentHandler

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

departs = getDepartment(url)
#print(departs)

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

deptinfo = dynamicMaxLimitHandler(departs)
#print(deptinfo)

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

deptUrls = departmentUrlHandler(deptinfo) #[1]
#print(departmentUrlHandler(deptinfo))
#print(len(deptUrls))


def departmentCourseContentHandler(deptCourseUrls):
    if deptCourseUrls[0] == False:
        return (False, [])
    else:
        deptUrls = deptCourseUrls[1]
        deptCourses = []
        for dept in deptUrls:
            dept_course_urls = getCourseContentHandler(dept)
            if dept_course_urls[0] == False:
                return (False, [])
            else:
                deptCourses.append(dept_course_urls[1])
    return (True, deptCourses)

deptCourseContent = departmentCourseContentHandler(deptUrls)
#print(deptCourseContent)
#print(len(deptCourseContent))

def prepCsv(deptCourseContent):
    if deptCourseContent[0] == False:
        return False
    else:
        departments = getDepartment(url)
        if departments[0] == False:
            return (False, [])
        else:
            if len(deptCourseContent[1]) == len(departments[1]):
                depart = departments[1]
                deptCourseInfo = deptCourseContent[1]
                csvInfo = []
                for dep, info in zip(depart, deptCourseInfo):
                    csvInfo.append((dep[1], info))
                return (True, csvInfo)
            else:
                return (False, [])

csvPreparedInformation = prepCsv(deptCourseContent)
#print(csvPreparedInformation)
#print(csvPreparedInformation))