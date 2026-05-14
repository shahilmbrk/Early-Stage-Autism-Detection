import numpy as np
import cv2
import os

# ----------------------------
# PATH TO YOUR .NPY DATASET
# ----------------------------
dataset_path = r"D:\Desktop\AUTISM\Video\Hand Flapping Classifier Dataset"

# Output folder for mp4
output_path = r"D:\Desktop\AUTISM\Video\Converted_Videos"
os.makedirs(output_path, exist_ok=True)

# Loop class folders
for cls in os.listdir(dataset_path):
    cls_path = os.path.join(dataset_path, cls)

    if not os.path.isdir(cls_path):
        continue

    print("CLASS:", cls)

    # Make output class folder
    cls_out = os.path.join(output_path, cls)
    os.makedirs(cls_out, exist_ok=True)

    # Loop subfolders
    for sub in os.listdir(cls_path):
        sub_path = os.path.join(cls_path, sub)

        if not os.path.isdir(sub_path):
            continue

        print("  Sub:", sub)

        # Make output subfolder
        sub_out = os.path.join(cls_out, sub)
        os.makedirs(sub_out, exist_ok=True)

        # Convert .npy to .mp4
        for file in os.listdir(sub_path):
            if file.endswith(".npy"):
                npy_file = os.path.join(sub_path, file)

                video_frames = np.load(npy_file)  # shape: (frames, h, w, 3)

                if len(video_frames.shape) != 4:
                    print("Skipping invalid file:", npy_file)
                    continue

                print("     Converting:", file)

                # Extract video info
                frames, H, W, C = video_frames.shape
                output_video = os.path.join(sub_out, file.replace(".npy", ".mp4"))

                # Video writer
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                fps = 20  # default fps
                out = cv2.VideoWriter(output_video, fourcc, fps, (W, H))

                for frame in video_frames:
                    frame = frame.astype('uint8')
                    out.write(frame)

                out.release()

print("Conversion Completed!")
