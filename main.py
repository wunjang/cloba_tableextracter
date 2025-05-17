import json
import asyncio
import aiohttp
import os
import uuid
import time
from pypdf import PdfReader, PdfWriter
from io import BytesIO

import data_client
import json_to_csv

with open('config.json', 'r') as f:
    CONFIG = json.load(f)

def load_images():
    folder_path = CONFIG['image_path']
    allowed_extensions = CONFIG['allowed_extensions']
    image_info_list = []
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                for ext in allowed_extensions:
                    if filename.lower().endswith(ext):
                        image_info = {
                            'name': os.path.splitext(filename)[0],
                            'format': ext[1:],
                            'path': file_path,
                            }
                        image_info_list.append(image_info)
                        break
    except Exception:
        raise

    return image_info_list

async def split_pdf(pdf_info)->list:
    try:
        with open(pdf_info['path'], 'rb') as f:
            pdf_reader = PdfReader(f)
            separated_pages = []
            for i, page in enumerate(pdf_reader.pages):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(page)

                # 메모리 상의 바이너리 스트림 생성
                output_stream = BytesIO()
                pdf_writer.write(output_stream)
                output_stream.seek(0)

                separated_pages.append({
                    'name': f'{pdf_info['name']}_page{i}',
                    'format': 'pdf',
                    'file': output_stream,
                })
            return separated_pages
    except Exception as e:
        print(f'ERROR: split_pdf - {e}')
        raise

async def request_ocr(session, format, name, file):
    request_json = {
        'images': [
            {
                'format': format,
                'name': name
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
        form_data.add_field('file', file)
        response = await data_client.send_request_async(session, CONFIG['url'], headers, form_data) # Pass form_data
        result = await response.json()
    except Exception as e:
        print(f'ERROR: request_ocr - {e}, image: format:{format}, name:{name}')
    
    return result

async def export_output(output, file_name):
    try:
        json_to_csv.json_to_csv(output, CONFIG['output_path'] + file_name)
    except Exception as e:
        print(f'ERROR: export_output - {e}')
        raise

async def extract_table():
    image_info_list = load_images()
    try:
        os.makedirs(CONFIG['image_path'], exist_ok=True)
        os.makedirs(CONFIG['output_path'], exist_ok=True)
        async with aiohttp.ClientSession() as session:
            for image_info in image_info_list:
                if image_info['format'] == 'pdf':
                    for pdf in await split_pdf(image_info):
                        print(f'{pdf['name']}에서 표를 추출하는 중...')
                        output = await request_ocr(session, pdf['format'], pdf['name'], pdf['file'])
                        await export_output(output, pdf['name'])
                else:
                    with open(image_info['path'], 'rb') as f:
                        print(f'{image_info['name']}에서 표를 추출하는 중...')
                        output = await request_ocr(session, image_info['format'], image_info['name'], f)
                    await export_output(output, image_info['name'])
    except aiohttp.ClientError as e:
        print(f"Aiohttp client error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def main():
    asyncio.run(extract_table())

if __name__ == "__main__":
    main()