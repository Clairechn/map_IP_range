import re

def iter_rows(ws):
    for row in ws.iter_rows():
        yield [cell.value for cell in row]

def display_row(row):
    return [cell.value for cell in row]

def split_multi_IP(row):
    '''
    Split the text of a multi-line IP address into multiple single-line IP addresses
    '''
    all_IP = row[3]
    new_rows = []

    for IP in all_IP.split('\n'):
        new_row = list(row)
        new_row[3] = IP
        new_rows.append(new_row)

    return new_rows

def split_start_end_IP(row):
    '''
    Split IP address into start IP address and end IP address
    '''

    start_IP, end_IP = '', ''
    IP = row[3]

    if '(' in IP:
        # e.g. IP address: 140.116.133.(193-222)
        prefix = re.search(r'^([^\(])+', IP).group() # 140.116.113
        start = re.match(r'.*?\((.*)\-', IP).group(1) # 193
        end = re.match(r'.*?\-(.*)\)', IP).group(1) # 222
        start_IP = prefix + start # 140.116.133.193
        end_IP = prefix + end # 140.116.133.222
    elif '-' in IP:
        # e.g. IP address: 140.116.133.127-140.116.133.128
        start_IP = re.match(r'(.*)\-', IP).group(1) # 140.116.133.127
        end_IP = re.match(r'.*?\-(.*)', IP).group(1) # 140.116.133.128
    else:
        # e.g. IP address: 140.116.132.*
        start_IP = IP
        end_IP = IP
    
    row[4], row[5] = start_IP.replace('*', '255'), end_IP.replace('*', '255')
    
    return row

def create_clean_data_list(column_list):
    clean_data = [column_list]
    return clean_data

def get_clean_data(pre_ws, clean_data):
    for i, row in enumerate(iter_rows(pre_ws)):
        if i > 0:
            try:
                # Split multi-line row into multiple single rows 
                if '\n' in row[3]:
                    new_rows = split_multi_IP(row)
                    for new_row in new_rows:
                        clean_row = split_start_end_IP(new_row)
                        clean_data.append(clean_row)
                else:
                    clean_row = split_start_end_IP(row)
                    clean_data.append(clean_row)
            except:
                continue

    return clean_data
    
    
