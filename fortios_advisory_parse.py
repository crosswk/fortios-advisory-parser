import requests
from bs4 import BeautifulSoup
import re

def get_vulnerability_list(version):
    """
    获取特定 FortiOS 版本的漏洞列表。

    Args:
        version (str): FortiOS 版本号。

    Returns:
        list: 一个列表，其中每个元素是一个包含漏洞信息的字典，格式为：
              [
                  {
                      'advisory_id': 'FG-IR-23-413',
                      'advisory_url': 'https://www.fortiguard.com/psirt/FG-IR-23-413'
                  },
                  ...
              ]
    """
    base_url = "https://www.fortiguard.com/psirt"
    vulnerability_list = []
    page = 1

    while True:
        url = f"{base_url}?page={page}&date=&severity=&product=FortiOS-6K7K,FortiOS&component=&version={version}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"请求失败，状态码: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')
        vulnerability_divs = soup.find_all('div', class_='row',
                                           onclick=lambda value: value and "location.href = '/psirt/" in value)

        if not vulnerability_divs:
            break  # 没有找到新的漏洞，退出循环

        for div in vulnerability_divs:
            onclick_value = div['onclick']
            match = re.search(r"location\.href = '/psirt/(.*?)'", onclick_value)

            if match:
                advisory_id = match.group(1)
                advisory_url = f"{base_url}/{advisory_id}"
                vulnerability_list.append({
                    'advisory_id': advisory_id,
                    'advisory_url': advisory_url
                })
        page += 1

    return vulnerability_list


def parse_fortigate_vulnerability(url):
    """
    解析 Fortigate 漏洞页面并提取相关信息。

    Args:
        url (str): Fortigate 漏洞页面的 URL。

    Returns:
        dict: 包含提取信息的字典，如果请求失败则返回 None。
            'affected_solution' 键现在包含一个人类可读的字符串，描述受影响的版本和解决方案。
             如果页面上找不到某个字段，对应的值会被设置为None
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return None
    soup = BeautifulSoup(response.content, 'html.parser')

    data = {}
    data['publication_url'] = url

    # 提取发布日期
    published_date_element = soup.find('td', string='Published Date')
    data['first_published'] = published_date_element.find_next_sibling('td').get_text(strip=True) if published_date_element else None

    # 提取更新日期
    updated_date_element = soup.find('td', string='Updated Date')
    data['last_updated'] = updated_date_element.find_next_sibling('td').get_text(strip=True) if updated_date_element else None

    # 提取严重性
    severity_element = soup.find('td', string='Severity')
    data['sir'] = severity_element.find_next_sibling('td').get_text(strip=True).strip() if severity_element else None

    # 提取 CVSSv3 分数
    cvss_element = soup.find('td', string='CVSSv3 Score')
    if cvss_element:
        cvss_link = cvss_element.find_next_sibling('td').find('a')
        data['cvss_base_score'] = cvss_link.get_text(strip=True) if cvss_link else None
    else:
       data['cvss_base_score'] = None

    # 提取影响
    impact_element = soup.find('td', string='Impact')
    data['impact'] = impact_element.find_next_sibling('td').get_text(strip=True) if impact_element else None


    # 提取 CVE ID
    cve_element = soup.find('td', string='CVE ID')
    if cve_element:
        cve_link = cve_element.find_next_sibling('td').find('a')
        data['cves'] = cve_link.get_text(strip=True) if cve_link else None
    else:
        data['cves']=None

    # 提取摘要
    summary_element = soup.find('h3', string='Summary')
    if summary_element:
      # 直接获取 <h3> 标签后的文本内容
      next_element = summary_element.next_sibling
      if next_element and isinstance(next_element, str):
         advisory_title = next_element.strip()
         data['advisory_title'] = advisory_title[:150] if len(advisory_title)>150 else advisory_title
      else:
         data['advisory_title'] = None
    else:
      data['advisory_title'] = None


    # 提取受影响的版本和解决方案，并格式化为字符串
    affected_solution_list = []
    table = soup.find('table')
    if table and table.find('tbody'):
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 3:
                affected_version = cells[1].get_text(strip=True)
                solution_version = cells[2].get_text(strip=True)
                affected_solution_list.append(f"受影响版本：{affected_version}，解决方案：{solution_version}")
    data['affected_solution'] = "、".join(affected_solution_list) if affected_solution_list else None
    return data


if __name__ == "__main__":
    # 获取指定版本的FortiOS漏洞列表
    fortios_vuln_url_list = get_vulnerability_list("6.4.0")
    print(fortios_vuln_url_list)

    fortios_vuln_list = []

    # 遍历漏洞URL列表，解析每个漏洞的详细信息
    for item in fortios_vuln_url_list:
        vulnerability_data = parse_fortigate_vulnerability(item['advisory_url'])

        if vulnerability_data:
            print(vulnerability_data)
            fortios_vuln_list.append(vulnerability_data)

    print(fortios_vuln_list)
