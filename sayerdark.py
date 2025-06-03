import requests
import time
import random
import json
import argparse
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from config import (
    TOR_SOCKS_PROXY, USER_AGENTS, KEYWORDS,
    PRODUCT_SELECTORS, PRICE_SELECTORS,
    MAX_RETRIES, TIMEOUT, REQUEST_DELAY,
    MAX_DEPTH, MAX_PAGES, CHECK_INTERVAL,
    MARKETS
)
from db import setup_db, add_or_update_product, update_market_status
from parsers import market1
from nlp_utils import analyze_text

# Global crawling variables
visited_pages = set()
site_structure = {
    'url': '',
    'title': '',
    'description': '',
    'pages': [],
    'forms': [],
    'links': [],
    'images': [],
    'scripts': [],
    'styles': [],
    'meta': {}
}

def print_banner():
    banner = """
    ==============================================
    ||                                          ||
    ||            S A Y E R  D A R K           ||
    ||                                          ||
    ==============================================
    
    [*] Developed by: SayerX
    [*] Version: 1.0.0
    [*] Web Market Monitor
    """
    print(banner)

def reset_crawler():
    """Reset crawler variables"""
    global visited_pages, site_structure
    visited_pages.clear()
    site_structure = {
        'url': '',
        'title': '',
        'description': '',
        'pages': [],
        'forms': [],
        'links': [],
        'images': [],
        'scripts': [],
        'styles': [],
        'meta': {}
    }

def get_random_user_agent():
    """Get a random user agent from the list"""
    return random.choice(USER_AGENTS)

def is_valid_url(url):
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def extract_meta_info(soup):
    """Extract meta information from the page"""
    meta_info = {}
    
    # Extract title
    title = soup.find('title')
    if title:
        meta_info['title'] = title.text.strip()
    
    # Extract description
    description = soup.find('meta', attrs={'name': 'description'})
    if description:
        meta_info['description'] = description.get('content', '')
    
    # Extract keywords
    keywords = soup.find('meta', attrs={'name': 'keywords'})
    if keywords:
        meta_info['keywords'] = keywords.get('content', '')
    
    return meta_info

def extract_forms(soup, page_url):
    """Extract forms from the page"""
    forms = []
    for form in soup.find_all('form'):
        form_info = {
            'action': urljoin(page_url, form.get('action', '')),
            'method': form.get('method', 'get'),
            'inputs': []
        }
        
        for input_field in form.find_all(['input', 'select', 'textarea']):
            input_info = {
                'type': input_field.get('type', 'text'),
                'name': input_field.get('name', ''),
                'id': input_field.get('id', ''),
                'required': input_field.get('required', False)
            }
            form_info['inputs'].append(input_info)
        
        forms.append(form_info)
    return forms

def extract_resources(soup, page_url):
    """Extract resources from the page"""
    resources = {
        'images': [],
        'scripts': [],
        'styles': []
    }
    
    # Extract images
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src:
            resources['images'].append({
                'url': urljoin(page_url, src),
                'alt': img.get('alt', '')
            })
    
    # Extract scripts
    for script in soup.find_all('script'):
        src = script.get('src', '')
        if src:
            resources['scripts'].append(urljoin(page_url, src))
    
    # Extract CSS files
    for style in soup.find_all('link', rel='stylesheet'):
        href = style.get('href', '')
        if href:
            resources['styles'].append(urljoin(page_url, href))
    
    return resources

def extract_products(html, url):
    """Extract products from the page with improved display"""
    soup = BeautifulSoup(html, 'html.parser')
    products = []
    
    # Search for products using all selectors
    for selector in PRODUCT_SELECTORS:
        for product in soup.select(selector):
            try:
                # Search for title
                title = None
                for h in product.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                    if h.text.strip():
                        title = h.text.strip()
                        break
                
                # Search for price
                price = None
                for price_selector in PRICE_SELECTORS:
                    price_elem = product.select_one(price_selector)
                    if price_elem and price_elem.text.strip():
                        price = price_elem.text.strip()
                        break
                
                # Search for description
                description = None
                desc_elem = product.find(['p', 'div'], class_=['description', 'details', 'info'])
                if desc_elem:
                    description = desc_elem.text.strip()
                
                # Search for image
                image = None
                img_elem = product.find('img')
                if img_elem and img_elem.get('src'):
                    image = urljoin(url, img_elem['src'])
                
                if title and price:
                    product_info = {
                        'title': title,
                        'price': price,
                        'url': url,
                        'description': description,
                        'image': image
                    }
                    products.append(product_info)
                    print(f"\n[+] Product Found:")
                    print(f"    Title: {title}")
                    print(f"    Price: {price}")
                    if description:
                        print(f"    Description: {description[:100]}...")
                    if image:
                        print(f"    Image: {image}")
            except Exception as e:
                print(f"[!] Error extracting product: {e}")
    
    return products

def check_tor_connection():
    """Check if Tor is running and accessible"""
    try:
        print("[*] Checking Tor connection...")
        # Try multiple Tor check URLs
        check_urls = [
            'https://check.torproject.org/',
            'http://check.torproject.org/',
            'https://torproject.org/'
        ]
        
        for url in check_urls:
            try:
                response = requests.get(
                    url,
                    proxies=TOR_SOCKS_PROXY,
                    timeout=30,
                    verify=False  # Disable SSL verification
                )
                if 'Congratulations' in response.text or 'Tor Project' in response.text:
                    print("[+] Tor connection successful!")
                    return True
            except requests.exceptions.SSLError:
                continue
            except requests.exceptions.RequestException:
                continue
        
        print("[!] Could not verify Tor connection")
        return False
        
    except Exception as e:
        print(f"[!] Tor connection error: {str(e)}")
        print("[*] Please check if Tor is running and properly configured")
        return False

def setup_proxies(url):
    """Setup appropriate proxy based on site type"""
    if ".onion" in url:
        if not check_tor_connection():
            print("[!] Cannot access .onion sites without working Tor connection")
            print("[*] Please ensure Tor is running and properly configured")
            print("[*] You can start Tor service using: sudo service tor start")
            return None
        print("[*] Using Tor for dark web access")
        return TOR_SOCKS_PROXY
    else:
        print("[*] Direct connection to site")
    return None

def extract_links(html, base_url):
    """Extract all valid links from HTML content"""
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(base_url, href)
        if is_valid_url(full_url):
            links.add(full_url)
    
    return links

def crawl_page(url, depth=0, visited=None, mode='products'):
    """
    Crawl a page and extract products or site structure
    mode: 'products' or 'structure'
    """
    if visited is None:
        visited = set()
    
    if depth > MAX_DEPTH or url in visited:
        return
    
    visited.add(url)
    print(f"\n[*] Analyzing page: {url}")
    
    try:
        # Get random user agent
        headers = {
            'User-Agent': get_random_user_agent()
        }
        
        # Setup proxy
        proxies = setup_proxies(url)
        if not proxies and ".onion" in url:
            print(f"[!] Cannot access .onion site without Tor: {url}")
            return
        
        # Make request with retries
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(
                    url,
                    proxies=proxies,
                    headers=headers,
                    timeout=TIMEOUT,
                    verify=False  # Disable SSL verification
                )
                response.raise_for_status()
                break
            except requests.exceptions.SSLError:
                print("[!] SSL Error - Retrying without verification...")
                continue
            except requests.exceptions.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    raise
                print(f"[!] Attempt {attempt + 1} failed: {str(e)}")
                time.sleep(REQUEST_DELAY)
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if mode == 'products':
            # Extract products
            products = extract_products(response.text, url)
            if products:
                print(f"\n[+] Found {len(products)} products on {url}")
                for product in products:
                    add_or_update_product("target", product['title'], product['price'], product['url'])
            else:
                print(f"[!] No products found on {url}")
        else:  # mode == 'structure'
            # Extract site structure
            page_info = {
                'url': url,
                'meta': extract_meta_info(soup),
                'forms': extract_forms(soup, url),
                'resources': extract_resources(soup, url),
                'links': []
            }
            
            # Extract links
            links = extract_links(response.text, url)
            if links:
                print(f"[+] Found {len(links)} links on {url}")
                for link in links:
                    page_info['links'].append({
                        'url': link,
                        'text': soup.find('a', href=link).text.strip() if soup.find('a', href=link) else ''
                    })
            else:
                print(f"[!] No links found on {url}")
            
            # Update site structure
            site_structure['pages'].append(page_info)
        
        # Follow links if not at max depth
        if depth < MAX_DEPTH:
            links = extract_links(response.text, url)
            for link in links:
                if link not in visited and not any(x in link for x in ['checkout', 'cart', 'login', 'register']):
                    time.sleep(REQUEST_DELAY)
                    crawl_page(link, depth + 1, visited, mode)
                    
    except requests.exceptions.RequestException as e:
        print(f"[!] Error crawling {url}: {str(e)}")
    except Exception as e:
        print(f"[!] Unexpected error crawling {url}: {str(e)}")

def save_site_structure(structure, base_url):
    """Save site structure to JSON file"""
    filename = f"site_map_{urlparse(base_url).netloc}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=4, ensure_ascii=False)
    print(f"[+] Site map saved to: {filename}")

def monitor_products(target_url):
    """Monitor products"""
    setup_db()
    
    # Check Tor connection first
    if ".onion" in target_url and not check_tor_connection():
        print("[!] Cannot monitor .onion sites without Tor")
        return
    
    print(f"[*] Using proxy: {setup_proxies(target_url)}")
    
    while True:
        try:
            print(f"\n[+] Checking site: {target_url}")
            crawl_page(target_url, mode='products')
            print(f"[*] Waiting {CHECK_INTERVAL} seconds before next round...")
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\n[*] Stopping monitoring...")
            break
        except Exception as e:
            print(f"[!] Error: {e}")
            time.sleep(10)

def map_site(url):
    """Map site structure"""
    global visited_pages, site_structure
    
    print(f"[*] Starting site mapping: {url}")
    reset_crawler()
    
    # Update basic site information
    site_structure['url'] = url
    
    # Start crawling
    crawl_page(url, mode='structure')
    
    # Check results and save
    if len(visited_pages) > 0:
        save_site_structure(site_structure, url)
        print(f"[+] Analyzed {len(visited_pages)} pages from {url}")
    else:
        print(f"[!] Failed to analyze site: {url}")

def get_target_url():
    print("\n[*] Enter target URL:")
    print("[*] For regular sites: http://example.com")
    print("[*] For dark web: http://example.onion")
    while True:
        url = input("> ").strip()
        if url.startswith("http://") or url.startswith("https://"):
            return url
        print("[!] Invalid URL. Must start with http:// or https://")

def select_mode():
    print("\n[*] Select crawling mode:")
    print("1. Monitor products and prices")
    print("2. Extract site structure")
    while True:
        try:
            choice = int(input("> "))
            if choice in [1, 2]:
                return "products" if choice == 1 else "structure"
            print("[!] Please choose 1 or 2")
        except ValueError:
            print("[!] Please enter a valid number")

def main():
    print_banner()
    
    # Get target URL
    target_url = get_target_url()
    
    # Select crawling mode
    mode = select_mode()
    
    if mode == "products":
        print(f"\n[*] Starting product monitoring for: {target_url}")
        monitor_products(target_url)
    else:
        print(f"\n[*] Starting site structure extraction: {target_url}")
        map_site(target_url)

if __name__ == "__main__":
    main()
