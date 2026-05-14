import os
from PIL import Image

# Folder path
folder_path = r"C:\Users\USER\Music\dataset\dataset\unknown"

for filename in os.listdir(folder_path):
    if filename.lower().endswith(".gif"):
        gif_path = os.path.join(folder_path, filename)

        try:
            with Image.open(gif_path) as img:
                rgb_img = img.convert("RGB")

                # Same name, only extension changed
                new_filename = os.path.splitext(filename)[0] + ".png"
                jpg_path = os.path.join(folder_path, new_filename)

                # Save as JPG
                rgb_img.save(jpg_path, "PNG")

            # Delete original GIF
            os.remove(gif_path)

            print(f"Replaced: {filename} → {new_filename}")

        except Exception as e:
            print(f"Error converting {filename}: {e}")

print("✅ All GIF files replaced with JPG successfully!")
