import os
import re

def cleanup_branding():
    base_dir = r"c:\Users\admin\Desktop\dripnest - Copy"
    
    # We will use local paths for images. 
    # Since we are serving from the root, 'framerusercontent.com/images/purple_dress_1.png' should work.
    
    js_fix = """
    <script id="dripnest-branding-fix">
      (function() {
        const productMap = {
          "Retro Handheld Console": "Royal Purple Anarkali",
          "Horizon Glow Sneakers": "Elegant Purple Saree",
          "Tropical Paradise Plant": "Lavender Designer Gown",
          "Vibrant Work Boots": "Violet Kurti Set",
          "Vintage Mechanical Keyboard": "Purple Silk Dupatta",
          "Pro Audio Mixer": "Deep Velvet Lehenga",
          "Potted Succulent Plant": "Plum Silk Kurta",
          "Modern Lounge Armchair": "Royal Purple Sherwani"
        };
        
        const priceMap = {
          "$59.99": "$199.99",
          "$129.99": "$249.99",
          "$39.99": "$179.99",
          "$89.99": "$159.99",
          "$149.99": "$299.99",
          "$199.99": "$399.99",
          "$19.99": "$89.99"
        };

        const imageMap = {
          "oCDAVYb409OovtE2SNLVIPK7zxk": "purple_dress_1.png",
          "TaiLqg44CMxGOXKWtD4HkafU": "purple_dress_2.png",
          "tElJe5z6jmy6md1MRCKy40PRUc": "purple_dress_3.png",
          "gFQCuW9AckxJjPOJEJbsnZIUTo": "purple_dress_4.png",
          "SLDtH0ehQK8jTan94MzwoAOWuQ": "purple_dress_1.png", // reusing for others
          "ZuZNJXHilGW5jzE1Qgvldb8Ko": "purple_dress_2.png"
        };

        function fixEverything() {
          // 1. Hide Branding
          const selectors = [
            '.buy-now', '#__framer-badge-container', '.framer-badge', 
            'a[href*="framer.com"]', 'div[aria-label*="Framer"]',
            'div[style*="z-index: 2000000000"]', 'div[style*="z-index: 2147483647"]',
            '.frameship-badge', '#frameship-banner', '.frameship-contents',
            'div[style*="position: fixed"][style*="bottom: 0px"]' // catch-all for bottom banners
          ];
          selectors.forEach(s => {
            document.querySelectorAll(s).forEach(el => {
               if (!el.id.includes('dripnest')) {
                  el.style.setProperty('display', 'none', 'important');
                  el.style.setProperty('visibility', 'hidden', 'important');
               }
            });
          });

          // 2. Transform Content
          const all = document.querySelectorAll('h1, h2, h3, h4, span, p, a, div, title');
          all.forEach(el => {
            // Text Logo
            if (el.textContent === 'Commerce_') el.textContent = 'DripNest_';
            
            // Products & Prices
            let text = el.textContent || "";
            for (const [old, newVal] of Object.entries(productMap)) {
               if (text.includes(old)) el.textContent = text.replace(old, newVal);
            }
            for (const [old, newVal] of Object.entries(priceMap)) {
               if (text.includes(old)) el.textContent = text.replace(old, newVal);
            }
            
            // Banner text removal
            if (text.includes('UPGRADE TO UNLOCK') || text.includes('Unlock ECOMMERCE')) {
               el.closest('div').style.setProperty('display', 'none', 'important');
            }
          });

          // 3. Transform Images
          document.querySelectorAll('img, div[style*="background-image"]').forEach(el => {
             const style = el.getAttribute('style') || "";
             const src = el.getAttribute('src') || "";
             for (const [id, newImg] of Object.entries(imageMap)) {
                if (src.includes(id) || style.includes(id)) {
                   const newPath = '/framerusercontent.com/images/' + newImg;
                   if (el.tagName === 'IMG') {
                      if (el.src !== newPath) el.src = newPath;
                   } else {
                      if (!style.includes(newImg)) el.style.backgroundImage = `url("${newPath}")`;
                   }
                }
             }
          });
        }
        
        fixEverything();
        setInterval(fixEverything, 300);
        window.addEventListener('load', fixEverything);
      })();
    </script>
    <style>
      .buy-now, #__framer-badge-container, .framer-badge, .frameship-badge, #frameship-banner {
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
                    
                    # Remove old fixes
                    content = re.sub(r'<script id="dripnest-branding-fix">.*?</script>', '', content, flags=re.DOTALL)
                    
                    # Inject JS/Style
                    if "</head>" in content:
                        content = content.replace("</head>", f"{js_fix}\n</head>")
                    
                    # Static replacements for SEO/Initial Load
                    content = content.replace("Commerce", "DripNest")
                    content = content.replace("Retro Handheld Console", "Royal Purple Anarkali")
                    content = content.replace("Horizon Glow Sneakers", "Elegant Purple Saree")
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                except Exception as e:
                    print(f"Error {file_path}: {e}")

if __name__ == "__main__":
    cleanup_branding()
