from dotenv import load_dotenv
import requests
import os
import json

'''
Return : records    : Rows of the navgurkul database in Notion
                    : {properties : field : {}}
'''
def get_navgurkul_records():
    all_records_resp = requests.post( f'https://api.notion.com/v1/databases/{NAVGURUKUL_DB_ID}/query', headers={ 'Authorization' : NOTION_TOKEN,  'Notion-Version' : NOTION_VERSION } )
    if all_records_resp.status_code == 200 :
        # print(all_records_resp.json(), "all_records_resp.json()")
        return all_records_resp.json()
    else :
        return {'Error' : all_records_resp.headers}

if __name__ == '__main__':
    load_dotenv()
    NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
    NOTION_VERSION = os.environ.get('NOTION_VERSION')
    NAVGURUKUL_DB_ID = os.environ.get('NAVGURUKUL_DB_ID')

    '''
    Steps -
    0. Pull data from DB
    1. Parse the data
    2. Rewrite different files like -
        navgurukul-openings.json
        navgurukul-team.json
        ...
    '''

    # Step 0. Get the data
    navgurkul_res = get_navgurkul_records()
    
    # Step 1. Parse the data. Currently, only two columns => {name, tag}
    '''
    Notion already has an ID to store each record.
    We will use thid "id" as our key as well
    '''
    navgrukul_db_dump = {}
    for row in navgurkul_res['results']:
        print(row, "row\n\n")
        id = row['id']
        # record_description = requests.get( f'https://api.notion.com/v1/blocks/{id}/children', headers={ 'Authorization' : NOTION_TOKEN,  'Notion-Version' : NOTION_VERSION })
        # print(record_description.json(), "record_description\n\n")
        row = row['properties']
        navgrukul_db_dump[id] = {}
        navgrukul_db_dump[id]['Name'] = row['Name']['title'][0]['plain_text']
        # print(navgrukul_db_dump[id]['Name'], "Name")
        navgrukul_db_dump[id]['Email'] = row['Email']['email'] if ('Email') in row else None
        navgrukul_db_dump[id]['Phone_number'] = row['Phone no.']['phone_number'] if ('Phone no.') in row else None
        navgrukul_db_dump[id]['Country'] = row['Country']['select']['name'] if ('Country') in row else None
        # print(row['LinkedIn']['rich_text'][0]['text']['content'], "row['LinkedIn']['content']\n\n")
        # print(row['Photo']['files'][0]['file']['url'], "photo\n\n")
        # navgrukul_db_dump[id]['LinkedIn'] = row['LinkedIn']['rich_text'][0]['text']['content'] if ('LinkedIn') in row else None
        # navgrukul_db_dump[id]['Skills'] = list(map(lambda x: x['name'], row['Skills']['multi_select']))
        navgrukul_db_dump[id]['Skills'] = list(map(lambda x: x['name'], row['Area of expertise/skills']['multi_select'] if ("Area of expertise/skills") in row else []))
        navgrukul_db_dump[id]['Association'] = row['Association']['select']['name'] if ('Association') in row else None
        # navgrukul_db_dump[id]['Photo'] = row['Photo']['files'][0]['file']['url'] if ('Photo') in row else None

    # Step 3. Dump data to tmp/navgurukul_testing.json
    with open('tmp/navgurkul_testing.json', 'w+') as json_file:
        json.dump(navgrukul_db_dump, json_file, indent=2)




