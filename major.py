import requests
from bs4 import BeautifulSoup

def getPage(url):
    request = requests.get(url)
    if request.status_code != 200:
        return (False, [])
    return (True, request.content)

def getUrls(baseUrl_and_Limit):
    url = baseUrl_and_Limit[0]
    limit = str(baseUrl_and_Limit[1]) 
    base_url = url + limit
    data = getPage(base_url)

    if (data[0] == False):
        return (False, [])
    else:
        soup = BeautifulSoup(data[1], 'html.parser')
        course_feed = soup.find('ul', class_="course-feed") 
        if course_feed:
            links = [li.find('a')['href'] for li in course_feed.find_all('li') if li.find('a')]
            return (True, links)
        else:
            return (False, [])

def dynamicMaxLimit(deptUrl):
    max_limit = 1
    while True: 
        base_url = deptUrl + str(max_limit)
        data = getPage(base_url)
        if (data[0] == False):
            return (False, [])
        else:
            soup = BeautifulSoup(data[1], 'html.parser')
            course_feed = soup.find('ul', class_="course-feed") 
            if course_feed and course_feed.find_all('li'):
                max_limit += 1
            else:
                max_limit -= 1
                break
    return (True, max_limit)

def getUrlsHandler(baseUrl_and_maxLimit):
    base_url = baseUrl_and_maxLimit[0] 
    max_limit = baseUrl_and_maxLimit[1] 
    limit = 1
    links_array = []
    while limit <= max_limit:
        if (getUrls((base_url, limit)) == (False, [])):
            return (False, [])
        else:
            data = getUrls((base_url, limit))
            links_array += data[1]
        limit += 1
    return (True, links_array)

def getCourseContent(url):
    courseContent = {}
    data = getPage(url)
    if (data[0] == False):
        return (False, [])
    else:
        soup = BeautifulSoup(data[1], 'html.parser')
        course_code = soup.h2.text
        courseContent['Course Code'] = course_code

        h1_elements = soup.find_all('h1')
        course_name = h1_elements[1].text.strip()
        courseContent['Course Name'] = course_name

        course_content_div = soup.find('div', id='course-content')
        if course_content_div:
            first_paragraph_text = course_content_div.find('p').get_text()
            courseContent['Course Description'] = first_paragraph_text

        offerings_ul = soup.find('ul', class_="cf-hub-offerings")
        if offerings_ul:  
            bu_hubs = [li.text.strip() for li in offerings_ul.find_all('li')]
            hubs = ""
            for hub in bu_hubs:
                hubs += " " +hub
            courseContent['Hub Units'] = hubs
        else:
            hubs = "None"
            courseContent['Hub Units'] = hubs

        info_box_div = soup.find('div', id="info-box")
        dd_elements = info_box_div.find_all('dd')
        if len(dd_elements) == 1:
            credit = dd_elements[0].text.strip() 
            prereqs = "None"
            courseContent['Prerequisites'] = prereqs
            courseContent['Credits'] = credit
        else:
            credit = dd_elements[0].text.strip() 
            prereqs = dd_elements[1].text.strip()
            courseContent['Prerequisites'] = prereqs
            courseContent['Credits'] = credit

        courseContent['link'] = url
        return (True, courseContent)

def getCourseContentHandler(urls):
    course_links = urls
    all_courses_info = []
    for link in course_links:
        base_url = "https://www.bu.edu/"
        course_info = getCourseContent(base_url + link)
        if course_info[0] == False:
            return (False, [])
        else:
            all_courses_info.append(course_info[1])
    return (True, all_courses_info)
