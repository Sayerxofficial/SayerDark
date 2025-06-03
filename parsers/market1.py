from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = []
    
    # Print HTML structure for verification
    print("\n[*] Analyzing product structure:")
    
    # Find all sections containing products
    sections = soup.find_all('div', class_='container')
    for section in sections:
        # Find section titles
        h2 = section.find('h2')
        if h2:
            section_title = h2.text.strip()
            print(f"\n[*] Section: {section_title}")
            
            # Find products in this section
            product_containers = section.find_all('div', class_='product-container')
            for container in product_containers:
                try:
                    # Get title
                    title = section_title
                    
                    # Get price from span
                    price_span = container.find('span')
                    if price_span:
                        price = price_span.text.strip()
                        if price and not price.startswith('('):  # Avoid text starting with (
                            products.append({
                                'title': title,
                                'price': price
                            })
                            print(f"[+] Product: {title} - {price}")
                except Exception as e:
                    print(f"[!] Error parsing product: {e}")
    
    print(f"\n[*] Total products discovered: {len(products)}")
    return products

def parse_products(html, url):
    """
    Parse products from HTML with improved error handling
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        products = []
        
        # Find all product containers
        product_containers = soup.find_all('div', class_='product-container')
        
        if not product_containers:
            print("No product containers found. Checking alternative selectors...")
            # Try alternative selectors
            product_containers = soup.find_all(['div', 'article'], class_=['product', 'item', 'listing'])
        
        for container in product_containers:
            try:
                # Extract title with validation
                title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'a'], class_=['title', 'name', 'product-title'])
                if not title_elem:
                    continue
                title = title_elem.text.strip()
                if not title:
                    continue
                
                # Extract price with validation
                price_elem = container.find(['span', 'div'], class_=['price', 'amount', 'product-price'])
                if not price_elem:
                    continue
                price_text = price_elem.text.strip()
                if not price_text:
                    continue
                
                # Clean and validate price
                try:
                    price = float(price_text.replace('$', '').replace(',', '').strip())
                except ValueError:
                    continue
                
                # Extract URL
                url_elem = container.find('a', href=True)
                product_url = urljoin(url, url_elem['href']) if url_elem else url
                
                products.append({
                    'title': title,
                    'price': price,
                    'url': product_url
                })
                
            except Exception as e:
                print(f"Error parsing product container: {str(e)}")
                continue
        
        return products
        
    except Exception as e:
        print(f"Error parsing HTML: {str(e)}")
        return []
