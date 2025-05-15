import json
import asyncio
import aiohttp
import os
import uuid
import time
import data_client
import json_to_csv

with open('config.json', 'r') as f:
    CONFIG = json.load(f)

def load_images(folder_path:str):
    allowed_extensions = CONFIG['allowed_extensions']
    image_list = []
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                for ext in allowed_extensions:
                    if filename.lower().endswith(ext):
                        image_list.append({
                            'name':os.path.splitext(filename)[0],
                            'format':ext[1:],
                            'path':file_path,
                            })
                        break
    except FileNotFoundError:
        print(f"Error: Folder not found at {folder_path}")
    
    except Exception as e:
        print(e)

    return image_list

async def request_ocr(session, image):
    request_json = {
        'images': [
            {
                'format': image['format'],
                'name': image['name']
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000)),
        'lang': 'ko',
        'enableTableDetection': True
    }
    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    headers = {
        'X-OCR-SECRET': CONFIG['API_KEY']
    }

    form_data = aiohttp.FormData()
    form_data.add_field('message', payload['message'].decode('UTF-8'))

    try:
        with open(image['path'], 'rb') as f:
            form_data.add_field('file', f)
            response = await data_client.send_request_async(session, CONFIG['url'], headers, form_data) # Pass form_data
            result = await response.json()
    except Exception as e:
        print(f'ERROR: request_ocr - {e}')
        raise
    
    return result

async def export_output(output, file_name):
    try:
        json_to_csv.json_to_csv(output, CONFIG['output_path'] + file_name)
    except Exception as e:
        print(f'ERROR: export_output - {e}')
        raise
    return

async def extract_table():
    image_list = load_images(CONFIG['image_path'])
    try:
        async with aiohttp.ClientSession() as session:
            for image in image_list:
                output = await request_ocr(session, image)
                await export_output(output, image['name'])
    except aiohttp.ClientError as e:
        print(f"Aiohttp client error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    return

def main():
    asyncio.run(extract_table())


if __name__ == "__main__":
    main()
