import os
import xml.etree.ElementTree as ET

# Corrected paths based on your terminal output
xml_folder = "labeled"  # Folder where XML files are stored
yolo_folder = "yolo"  # Folder where converted YOLO files will be saved

# Ensure YOLO folder exists
os.makedirs(yolo_folder, exist_ok=True)

# Define class names (Make sure it matches your labeling)
class_names = ["climbing"]

# Convert function
def convert_voc_to_yolo(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    img_width = int(root.find("size/width").text)
    img_height = int(root.find("size/height").text)

    yolo_labels = []
    for obj in root.findall("object"):
        class_name = obj.find("name").text
        if class_name not in class_names:
            continue  # Skip if class is not recognized
        
        class_id = class_names.index(class_name)

        bbox = obj.find("bndbox")
        xmin = int(bbox.find("xmin").text)
        ymin = int(bbox.find("ymin").text)
        xmax = int(bbox.find("xmax").text)
        ymax = int(bbox.find("ymax").text)

        # Normalize to YOLO format
        x_center = (xmin + xmax) / 2 / img_width
        y_center = (ymin + ymax) / 2 / img_height
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height

        yolo_labels.append(f"{class_id} {x_center} {y_center} {width} {height}")

    # Save YOLO labels
    txt_filename = os.path.join(yolo_folder, os.path.basename(xml_file).replace(".xml", ".txt"))
    with open(txt_filename, "w") as f:
        f.write("\n".join(yolo_labels))

# Process all XML files
if not os.path.exists(xml_folder):
    print(f"❌ Error: XML folder '{xml_folder}' not found!")
    exit()

xml_files = [f for f in os.listdir(xml_folder) if f.endswith(".xml")]

if not xml_files:
    print(f"❌ Error: No XML files found in '{xml_folder}'")
    exit()

for xml_file in xml_files:
    convert_voc_to_yolo(os.path.join(xml_folder, xml_file))

print("✅ XML to YOLO conversion completed!")
