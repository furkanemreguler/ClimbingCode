import cv2
import os

# Set paths
video_folder = "videos/tirmanma"  # Folder with input videos
output_folder = "videos/frames"   # Folder to save extracted images

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# List all video files
video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]

if not video_files:
    print("❌ No video files found in", video_folder)
else:
    print(f"✅ Found {len(video_files)} videos: {video_files}")

# Extract frames from each video
for video_file in video_files:
    video_path = os.path.join(video_folder, video_file)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"❌ Failed to open {video_file}")
        continue

    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"📹 Processing {video_file} at {fps} FPS")

    frame_rate = 30  # Extract 2 frames per second
    frame_count = 0
    success, image = cap.read()

    while success:
        if frame_count % int(fps / frame_rate) == 0:
            frame_filename = os.path.join(output_folder, f"{video_file}_frame{frame_count}.jpg")
            cv2.imwrite(frame_filename, image)
            print(f"🖼️ Saved: {frame_filename}")
        
        success, image = cap.read()
        frame_count += 1

    cap.release()
    print(f"✅ Frames extracted from {video_file}")

print("🎉 Frame extraction completed!")
