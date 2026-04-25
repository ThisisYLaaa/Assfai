import os
import re
import requests
from urllib.parse import urlparse, urljoin

# 读取文件内容
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"读取文件失败: {file_path} - {str(e)}")
        return ""

# 提取所有链接
def extract_links(content):
    links = []
    
    # 提取content-ref中的链接
    content_ref_pattern = r'\{% content-ref url="(.*?)" %\}'
    content_ref_links = re.findall(content_ref_pattern, content)
    links.extend(content_ref_links)
    
    # 提取Markdown链接
    markdown_pattern = r'\[.*?\]\((https://.*?)\)'
    markdown_links = re.findall(markdown_pattern, content)
    links.extend(markdown_links)
    
    # 提取HTML中的<a href>链接
    html_link_pattern = r'<a\s+href="(.*?)"[^>]*>.*?</a>'
    html_links = re.findall(html_link_pattern, content)
    links.extend(html_links)
    
    return links

# 处理链接，添加.md扩展名
def process_links(links, base_url):
    processed_links = []
    
    for link in links:
        if link.startswith('http'):
            # 对于完整URL，确保以.md结尾
            if not link.endswith('.md'):
                link += '.md'
            processed_links.append(link)
        else:
            # 对于相对路径，转换为完整URL
            full_url = urljoin(base_url, link)
            if not full_url.endswith('.md'):
                full_url += '.md'
            processed_links.append(full_url)
    
    return processed_links

# 检查链接是否属于adofaieditor.gitbook.io域名
def is_valid_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == 'adofaieditor.gitbook.io'

# 下载文件
def download_file(url, save_dir):
    try:
        # 检查域名是否有效
        if not is_valid_domain(url):
            print(f"跳过非adofaieditor.gitbook.io域名的链接: {url}")
            return False, None
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # 解析URL，获取保存路径
        parsed_url = urlparse(url)
        path = parsed_url.path.lstrip('/')
        
        # 确保路径合法
        safe_path = os.path.normpath(path)
        file_path = os.path.join(save_dir, safe_path)
        
        # 创建目录
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 保存文件
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        print(f"下载成功: {url} -> {file_path}")
        return True, file_path
    except Exception as e:
        print(f"下载失败: {url} - {str(e)}")
        return False, None

# 递归下载函数
def recursive_download(urls, save_dir, downloaded_urls):
    success_count = 0
    new_urls = []
    
    for url in urls:
        if url in downloaded_urls:
            print(f"跳过已下载的链接: {url}")
            continue
        
        # 下载文件
        success, file_path = download_file(url, save_dir)
        if success:
            success_count += 1
            downloaded_urls.add(url)
            
            # 读取下载的文件内容，提取新链接
            content = read_file(file_path)
            if content:
                links = extract_links(content)
                base_url = url.rsplit('/', 1)[0] + '/' if '/' in url else url
                processed_links = process_links(links, base_url)
                
                # 过滤有效的链接
                for link in processed_links:
                    if link not in downloaded_urls and is_valid_domain(link):
                        new_urls.append(link)
    
    # 递归处理新链接
    if new_urls:
        print(f"发现 {len(new_urls)} 个新链接，开始递归下载...")
        new_success_count = recursive_download(new_urls, save_dir, downloaded_urls)
        success_count += new_success_count
    
    return success_count

# 主函数
def main():
    # 配置
    dictionary_file = "d:\\My WorkStation\\Assfai\\afgitbook\\Dictionary.md"
    save_dir = "d:\\My WorkStation\\Assfai\\afgitbook\\docs"
    base_url = "https://adofaieditor.gitbook.io/"
    
    # 确保保存目录存在
    os.makedirs(save_dir, exist_ok=True)
    
    # 读取Dictionary.md文件内容
    content = read_file(dictionary_file)
    
    # 提取链接
    links = extract_links(content)
    
    # 处理链接
    processed_links = process_links(links, base_url)
    
    # 去重
    unique_links = list(set(processed_links))
    
    # 过滤有效的链接
    valid_links = [link for link in unique_links if is_valid_domain(link)]
    
    # 开始递归下载
    print(f"开始下载 {len(valid_links)} 个初始文件...")
    downloaded_urls = set()
    success_count = recursive_download(valid_links, save_dir, downloaded_urls)
    
    print(f"下载完成，成功 {success_count} 个文件")

if __name__ == "__main__":
    main()
