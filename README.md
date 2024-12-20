# FortiOS 漏洞公告解析器 (FortiOS Advisory Parser)

## 简介

这个 Python 工具可以帮助你从 FortiGuard 网站解析 FortiOS 漏洞公告页面，提取关键信息，例如发布日期、严重性、CVSS 评分、影响以及受影响的版本和解决方案。该工具主要用于信息收集和分析，**而不是执行主动漏洞扫描**。

## 功能

*   **按版本解析:** 根据指定的 FortiOS 版本，从 FortiGuard 网站抓取相关漏洞公告的 URL 列表，并解析这些页面的内容。
*   **信息提取:** 从每个漏洞公告页面提取详细信息，包括：
    *   发布日期和更新日期
    *   严重性
    *   CVSSv3 评分
    *   影响描述
    *   CVE ID
    *   漏洞摘要
    *   受影响的版本和解决方案
*   **结构化输出:** 将提取的信息以 Python 字典的形式返回，方便后续处理和分析。
*   **易于使用:** 使用 Python 编写，易于安装和运行。

## 使用方法

### 1. 环境准备

确保你已经安装了 Python 3.6+ 和 `requests` 和 `beautifulsoup4` 库。你可以使用 pip 安装依赖：

```bash
pip install requests beautifulsoup4
```

### 2. 运行代码

1.  将 `fortios_vulnerability_parser.py` 文件保存到本地。
2.  打开终端或命令提示符，导航到保存 `fortios_vulnerability_parser.py` 文件的目录。
3.  运行以下命令，将 `[version]` 替换为你想要查询的 FortiOS 版本号（例如 `6.4.0`）：

```bash
python fortios_vulnerability_parser.py
```

   脚本会将该版本的漏洞列表和每个漏洞的详情打印到终端。

   你也可以通过修改`if __name__ == "__main__":` 部分的代码，实现调用和数据存储。

## 代码说明

*   `get_vulnerability_list(version)`:  从 FortiGuard 网站获取指定 FortiOS 版本的漏洞公告 URL 列表。
*   `parse_fortigate_vulnerability(url)`:  解析单个漏洞公告页面，提取相关信息。

## 输出格式

每个漏洞的详情以 Python 字典的形式返回，格式如下：

```python
{
    'publication_url': '漏洞公告页面 URL',
    'first_published': '发布日期',
    'last_updated': '更新日期',
    'sir': '严重性',
    'cvss_base_score': 'CVSSv3 评分',
    'impact': '影响描述',
    'cves': 'CVE ID',
    'advisory_title':'漏洞摘要',
    'affected_solution': '受影响的版本和解决方案（以字符串形式）'
}
```

**示例：**

以下是一个示例输出，展示了解析后的漏洞信息：

```python
{
    'publication_url': 'https://www.fortiguard.com/psirt/FG-IR-23-413',
    'first_published': 'Apr 9, 2024',
    'last_updated': 'Dec 2, 2024',
    'sir': 'Medium',
    'cvss_base_score': '6.1',
    'impact': 'Execute unauthorized code or commands',
    'cves': 'CVE-2023-48784',
    'advisory_title': '',
    'affected_solution': '受影响版本：7.4.0 through 7.4.1，解决方案：Upgrade to 7.4.2 or above、受影响版本：7.2.0 through 7.2.7，解决方案：Upgrade to 7.2.8 or above、受影响版本：7.0.0 through 7.0.15，解决方案：Upgrade to 7.0.16 or above、受影响版本：6.4 all versions，解决方案：Migrate to a fixed release'
}

{
    'publication_url': 'https://www.fortiguard.com/psirt/FG-IR-24-032',
    'first_published': 'Nov 12, 2024',
    'last_updated': 'Nov 15, 2024',
    'sir': 'Medium',
    'cvss_base_score': '5.2',
    'impact': 'Execute unauthorized code or commands',
    'cves': 'CVE-2024-26011',
    'advisory_title': '',
    'affected_solution': '受影响版本：7.4.0 through 7.4.2，解决方案：Upgrade to 7.4.3 or above、受影响版本：7.2.0 through 7.2.4，解决方案：Upgrade to 7.2.5 or above、受影响版本：7.0.0 through 7.0.11，解决方案：Upgrade to 7.0.12 or above、受影响版本：6.4.0 through 6.4.14，解决方案：Upgrade to 6.4.15 or above、受影响版本：Not affected，解决方案：Not Applicable、受影响版本：7.4.0 through 7.4.3，解决方案：Upgrade to 7.4.4 or above、受影响版本：7.2.0 through 7.2.7，解决方案：Upgrade to 7.2.8 or above、受影响版本：7.0.0 through 7.0.14，解决方案：Upgrade to 7.0.15 or above、受影响版本：6.4 all versions，解决方案：Migrate to a fixed release、受影响版本：6.2 all versions，解决方案：Migrate to a fixed release、受影响版本：6.0 all versions，解决方案：Migrate to a fixed release、受影响版本：Not affected，解决方案：Not Applicable、受影响版本：1.2 all versions，解决方案：Migrate to a fixed release、受影响版本：1.1 all versions，解决方案：Migrate to a fixed release、受影响版本：1.0 all versions，解决方案：Migrate to a fixed release、受影响版本：6.0.0 through 6.0.14，解决方案：Upgrade to 6.0.15 or above、受影响版本：5.3 all versions，解决方案：Migrate to a fixed release、受影响版本：7.4.0 through 7.4.3，解决方案：Upgrade to 7.4.4 or above、受影响版本：7.2.0 through 7.2.9，解决方案：Upgrade to 7.2.10 or above、受影响版本：7.0.0 through 7.0.16，解决方案：Upgrade to 7.0.17 or above、受影响版本：2.0 all versions，解决方案：Migrate to a fixed release、受影响版本：1.2 all versions，解决方案：Migrate to a fixed release、受影响版本：1.1 all versions，解决方案：Migrate to a fixed release、受影响版本：1.0 all versions，解决方案：Migrate to a fixed release、受影响版本：7.2.0 through 7.2.3，解决方案：Upgrade to 7.2.4 or above、受影响版本：7.0.0 through 7.0.3，解决方案：Upgrade to 7.0.4 or above'
}
```

## 注意事项

*   该工具需要网络连接才能访问 FortiGuard 网站。
*   FortiGuard 网站的结构可能会发生变化，导致代码失效。如果遇到问题，请及时更新代码或提交 Issue。
*   该工具仅用于信息收集和学习目的，请遵守相关法律法规。
*   **该工具不是漏洞扫描器，而是漏洞公告的解析器。**
*   目前`advisory_title`只截取了150个字符，你可以在代码中修改该值。
*   如果某个字段在网页上不存在，则会被设置为`None`
