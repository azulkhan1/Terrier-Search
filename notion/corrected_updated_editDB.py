import requests
import json
import re

NOTION_TOKEN = 'secret_tKsdODcmoS0hQNPBQ6Ew7zDjdGj83OU1Tv77pG2xTY2'

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'  
}

def fetch_database(database_id):
    fetch_url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(fetch_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching database: {response.text}")
    return response.json()

def update_course_with_link(database_items):
    for item in database_items['results']:
        page_id = item['id']
        course_name_texts = item['properties']['Course Name']['rich_text']
        course_name = "".join([text['text']['content'] for text in course_name_texts])
        link = item['properties']['link']['url']
        
        update_url = f'https://api.notion.com/v1/pages/{page_id}'
        update_data = json.dumps({
            'properties': {
                'Course Name': {
                    'rich_text': [
                        {'text': {'content': course_name, 'link': {'url': link}}}
                    ]
                }
            }
        })
        update_response = requests.request('PATCH', update_url, headers=headers, data=update_data)
        if update_response.status_code != 200:
            raise Exception(f'Error updating page: {update_response.text}')


database_id = '7dc4512c1acd491f8b8e1df4b8ae7836'
database_data = fetch_database(database_id)

update_course_with_link(database_data)


def process_text(text):
    split_phrases = [
        "Philosophical Inquiry and Life's Meanings", "Aesthetic Exploration", 
        "Historical Consciousness","Scientific Inquiry II", "Social Inquiry II",
        "Scientific Inquiry I", "Social Inquiry I", "Quantitative Reasoning II", 
        "Quantitative Reasoning I", "The Individual in Community", 
        "Global Citizenship and Intercultural Literacy", "Ethical Reasoning", 
        "First-Year Writing Seminar", "Writing Research and Inquiry", 
        "Writing-Intensive Course", "Oral and/or Signed Communication", 
        "Digital/Multimedia Expression", "Critical Thinking", 
        "Research and Information Literacy", "Teamwork/Collaboration", 
        "Creativity/Innovation"
    ]

    text = text.replace("Writing, Research, and Inquiry", "Writing Research and Inquiry")

    pattern = r'({})'.format('|'.join(map(re.escape, split_phrases)))

    split_text = re.split(pattern, text)

    processed = [piece.strip() for piece in split_text if piece.strip()]

    return processed


processed_data = []
for item in database_data["results"]:
    text_content = item['properties']['Hub Units']['rich_text']
    text = ''.join([rt['plain_text'] for rt in text_content if rt.get('plain_text')])
    tags = process_text(text)
    processed_data.append({'id': item['id'], 'tags': tags})


def update_item(item_id, tags):
    update_url = f"https://api.notion.com/v1/pages/{item_id}"
    data = {
        "properties": {
            "Hub(s)": {
                "multi_select": [{"name": tag} for tag in tags]
            }
        }
    }
    response = requests.patch(update_url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Error updating item: {response.text}")

for item in processed_data:
    update_item(item['id'], item['tags'])