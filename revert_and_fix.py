import os
import re

def revert_and_fix():
    base_dir = r"c:\Users\admin\Desktop\dripnest - Copy"
    
    js_fix = """
    <script id="dripnest-branding-fix">
      (function() {
        // High-level mapping for products
        const productMap = {
          "Retro Handheld Console": "Royal Purple Anarkali",
          "Horizon Glow Sneakers": "Elegant Purple Saree",
          "Tropical Paradise Plant": "Lavender Designer Gown",
          "Vibrant Work Boots": "Violet Kurti Set",
          "Vintage Mechanical Keyboard": "Purple Silk Dupatta"
        };
        
        const priceMap = {
          "$59.99": "$199.99",
          "$129.99": "$249.99",
          "$39.99": "$179.99"
        };

        const imageMap = {
          "oCDAVYb409OovtE2SNLVIPK7zxk": "purple_dress_1.png",
          "TaiLqg44CMxGOXKWtD4HkafU": "purple_dress_2.png",
          "tElJe5z6jmy6md1MRCKy40PRUc": "purple_dress_3.png"
        };

        function applyFixes() {
          // 1. Branding removal
          document.querySelectorAll('.buy-now, #__framer-badge-container, .framer-badge, .frameship-badge, #frameship-banner, .frameship-contents').forEach(el => {
            el.style.setProperty('display', 'none', 'important');
          });

          // 2. Text transformation
          document.querySelectorAll('h1, h2, h3, h4, span, p, a, div, title').forEach(el => {
            if (el.children.length > 0) return; // Only target leaf nodes
            let text = el.textContent || "";
            if (text === 'Commerce_') el.textContent = 'DripNest_';
            
            for (const [old, newVal] of Object.entries(productMap)) {
               if (text.includes(old)) el.textContent = text.replace(old, newVal);
            }
          });

          // 3. Image transformation
          document.querySelectorAll('img, div[style*="background-image"]').forEach(el => {
             const style = el.getAttribute('style') || "";
             const src = el.getAttribute('src') || "";
             for (const [id, newImg] of Object.entries(imageMap)) {
                if (src.includes(id) || style.includes(id)) {
                   const newUrl = '/framerusercontent.com/images/' + newImg;
                   if (el.tagName === 'IMG') { if (el.src !== newUrl) el.src = newUrl; }
                   else { if (!style.includes(newImg)) el.style.backgroundImage = `url("${newUrl}")`; }
                }
             }
          });
        }

        setInterval(applyFixes, 500);
      })();
    </script>
    <style>
      .buy-now, #__framer-badge-container, .framer-badge, .frameship-badge, #frameship-banner { display: none !important; }
    </style>
    """

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # 1. REVERT: Change all DripNest back to Commerce to fix breakages
                    # (This is a bit risky but we need to restore the technical strings)
                    # We'll avoid changing the title tag though.
                    
                    # Temporarily save titles
                    titles = re.findall(r'<title>.*?</title>', content, flags=re.IGNORECASE)
                    
                    # Revert everything else
                    content = content.replace("DripNest", "Commerce")
                    content = content.replace("Royal Purple Anarkali", "Retro Handheld Console")
                    content = content.replace("Elegant Purple Saree", "Horizon Glow Sneakers")
                    
                    # Put titles back (or set them to DripNest)
                    if titles:
                        content = re.sub(r'<title>.*?</title>', '<title>DripNest - Premium Indian Boutique</title>', content)
                    
                    # 2. FIX: Remove old scripts and inject the safe JS fix
                    content = re.sub(r'<script id="dripnest-branding-fix">.*?</script>', '', content, flags=re.DOTALL)
                    content = re.sub(r'<style>\s*/\* Injected by DripNest Branding Fix \*/.*?</style>', '', content, flags=re.DOTALL)
                    
                    if "</head>" in content:
                        content = content.replace("</head>", f"{js_fix}\n</head>")
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                except Exception as e:
                    print(f"Error {file_path}: {e}")

if __name__ == "__main__":
    revert_and_fix()
