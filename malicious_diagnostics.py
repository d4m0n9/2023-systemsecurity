import requests

def scan_file(api_key, file_path):
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': api_key}

    with open(file_path, 'rb') as file:
        files = {'file': (file_path, file)}
        response = requests.post(url, files=files, params=params)

    result = response.json()
    return result

def get_scan_report(api_key, resource):
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': api_key, 'resource': resource}

    response = requests.get(url, params=params)
    result = response.json()
    return result

def virus_scan(api_key, file_path):
    upload_result = scan_file(api_key, file_path)
    resource = upload_result['resource']
    report = get_scan_report(api_key, resource)
    return report
