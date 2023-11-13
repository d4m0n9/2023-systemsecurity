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

if __name__ == "__main__":
    # 'YOUR_API_KEY'를 실제 VirusTotal API key로 교체(지원's API)
    api_key = 'd00e049b5870f0f4b82b1ce1f5a3879e87575961e03122b934f982dc46e66c19'

    # 'file_to_upload.txt'의 파일 경로 교체
    file_path = input("Enter the path of the file: ")
    
    # 1단계: 스캔할 파일 업로드
    upload_result = scan_file(api_key, file_path)
    print("File uploaded for scanning. Resource: {}".format(upload_result['resource']))

    # 2단계: 검색이 완료될 때까지 대기(VirusTotal 정책에 따라 다름)
    # 3단계: 스캔 보고서 검색
    resource = upload_result['resource']
    report = get_scan_report(api_key, resource)

    # 4단계: 스캔 결과 인쇄
    print("Scan results:")
    print("  - Total scans: {}".format(report['total']))
    print("  - Positive scans: {}".format(report['positives']))
    print("  - Scan results: {}".format(report['scans']))
