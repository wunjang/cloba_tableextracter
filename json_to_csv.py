import csv

def json_to_csv(data, file_name):
    # Assuming you have one image and want the first table
    tables = data['images'][0]['tables']

    for i, table in enumerate(tables):
        cells = table['cells']

        # Determine the maximum number of columns and rows
        max_row_index = max(cell['rowIndex'] for cell in cells) + 1
        max_col_index = max(cell['columnIndex'] for cell in cells) + 1

        # Create an empty table structure (list of lists)
        csv_data = [['' for _ in range(max_col_index)] for _ in range(max_row_index)]

        for cellTextLines in cells:
            row_index = cellTextLines['rowIndex']
            col_index = cellTextLines['columnIndex']
            for cellWords in cellTextLines['cellTextLines']:
                cell_text = ' '.join(item['inferText'] for item in cellWords['cellWords'] if item.get('inferText'))
                csv_data[row_index][col_index] += cell_text
            
        with open(file_name + f'_{i}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)