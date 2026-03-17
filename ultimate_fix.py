import os
import re

def ultimate_fix_v2():
    base_dir = r"c:\Users\admin\Desktop\dripnest - Copy"
    
    js_fix = """
    <script id="dripnest-branding-fix">
      (function() {
        const productData = {
          "Retro Handheld Console": { title: "Royal Purple Anarkali", price: "$199.99", cat: "Clothing", img: "purple_dress_1.png" },
          "Horizon Glow Sneakers": { title: "Elegant Purple Saree", price: "$249.99", cat: "Ethnic Wear", img: "purple_dress_2.png" },
          "Tropical Paradise Plant": { title: "Lavender Designer Gown", price: "$179.99", cat: "Designer Wear", img: "purple_dress_3.png" },
          "Vintage Mechanical Keyboard": { title: "Purple Silk Dupatta", price: "$89.99", cat: "Accessories", img: "purple_dress_4.png" }
        };

        function applyReplacements() {
          // 1. Branding removal (Banner & Frameship)
          const brandingItems = [
            '.buy-now', '.framer-badge', '#__framer-badge-container', '.frameship-badge', 
            '#frameship-banner', '.frameship-contents', 'div[aria-label*="Framer"]',
            'a[href*="framer.com"]', 'a[href*="buy.hxmzaehsan.com"]'
          ];
          brandingItems.forEach(s => {
            document.querySelectorAll(s).forEach(el => {
              el.style.setProperty('display', 'none', 'important');
              el.style.setProperty('visibility', 'hidden', 'important');
            });
          });

          // 2. Text Logo & Category Replacements
          document.querySelectorAll('h1, h2, h3, h4, span, p, a, div, b, i').forEach(el => {
             if (el.children.length > 0) return;
             let text = el.textContent || "";
             
             // Global Replacements
             if (text.trim() === 'Commerce_') el.textContent = 'DripNest_';
             if (text.includes('UPGRADE TO UNLOCK') || text.includes('Unlock ECOMMERCE')) {
                const parent = el.closest('div[style*="position: fixed"]');
                if (parent) parent.style.setProperty('display', 'none', 'important');
             }

             // Product Mappings
             for (const [old, data] of Object.entries(productData)) {
               if (text.includes(old)) el.textContent = text.replace(old, data.title);
             }
             
             // Category & Price Mappings
             if (text === 'Technology' || text === 'Gadget') el.textContent = 'Clothing';
             if (text === 'Footwear') el.textContent = 'Ethnic Wear';
             if (text === 'Home') el.textContent = 'Designer Wear';
             
             if (text.includes('$59.99')) el.textContent = text.replace('$59.99', '$199.99');
             if (text.includes('$129.99')) el.textContent = text.replace('$129.99', '$249.99');
             if (text.includes('$39.99')) el.textContent = text.replace('$39.99', '$179.99');
          });

          // 3. Image Replacements (Using relative paths to bypass ORB)
          const imgMap = {
            "oCDAVYb409OovtE2SNLVIPK7zxk": "purple_dress_1.png",
            "TaiLqg44CMxGOXKWtD4HkafU": "purple_dress_2.png",
            "tElJe5z6jmy6md1MRCKy40PRUc": "purple_dress_3.png"
          };
          
          document.querySelectorAll('img, div[style*="background-image"]').forEach(el => {
            const style = el.getAttribute('style') || "";
            const src = el.getAttribute('src') || "";
            for (const [id, localName] of Object.entries(imgMap)) {
              if (src.includes(id) || style.includes(id)) {
                // Determine relative depth
                const depth = window.location.pathname.split('/').length - 2;
                const prefix = depth > 0 ? '../'.repeat(depth) : '';
                const newUrl = prefix + 'framerusercontent.com/images/' + localName;
                
                if (el.tagName === 'IMG') {
                  if (!el.src.includes(localName)) el.src = newUrl;
                } else {
                  if (!style.includes(localName)) el.style.backgroundImage = 'url("' + newUrl + '")';
                }
              }
            }
          });
        }

        setInterval(applyReplacements, 1000);
        window.addEventListener('load', applyReplacements);
      })();
    </script>
    <style>
      .buy-now, .framer-badge, #__framer-badge-container, .frameship-badge, #frameship-banner,
      div[style*="z-index: 2147483647"], div[style*="z-index: 2000000000"] {
        display: none !important;
      }
    </style>
    """

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Full Revert to baseline
                    content = re.sub(r'<script id="dripnest-branding-fix">.*?</script>', '', content, flags=re.DOTALL)
                    content = re.sub(r'<style>\s*/\* Injected by DripNest Branding Fix \*/.*?</style>', '', content, flags=re.DOTALL)
                    content = content.replace("Royal Purple Anarkali", "Retro Handheld Console")
                    content = content.replace("Elegant Purple Saree", "Horizon Glow Sneakers")
                    content = content.replace("Lavender Designer Gown", "Tropical Paradise Plant")
                    content = content.replace("DripNest", "Commerce")
                    
                    # Apply branding
                    content = re.sub(r'<title>.*?</title>', '<title>DripNest - Premium Indian Boutique</title>', content)
                    content = content.replace('content="Commerce', 'content="DripNest')
                    
                    # Inject JS fix
                    if "</head>" in content:
                        content = content.replace("</head>", f"{js_fix}\n</head>")
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                except Exception as e:
                    print(f"Error {file_path}: {e}")

if __name__ == "__main__":
    ultimate_fix_v2()
    print("Ultimate Fix v2 Applied.")
