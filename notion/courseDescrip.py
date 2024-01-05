from notion_client import Client

notion = Client(auth="") #Notion_API_TOKEN
database_id = "" #NOTION_DATABASE_ID

response = notion.databases.query(database_id)

for page in response['results']:
    page_id = page['id']
    
    course_description = page["properties"]["Course Description"]["rich_text"]

    if course_description:
        text_content = ''.join([rt["plain_text"] for rt in course_description])

        new_block = {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text_content,
                            "link": None
                        }
                    }
                ]
            }
        }

        notion.blocks.children.append(page_id, children=[new_block])
