from pathlib import Path
import json
import numpy as np
import pandas as pd

here = Path(__file__).parent.parent
fname = here / 'data/berlin/reconstruction_example.json'
fname2 = here / 'data/berlin/tracks_example.csv'
fname3 = here / 'data/berlin/reconstruction_03_test.json'

target_name = "03.jpg"

with fname.open() as f:
    json_data = json.load(f)
data = json_data[0]

# level 1
cameras = data["cameras"]
shots = data["shots"]
points = data["points"]
biases = data["biases"]
reference_lla = data["reference_lla"]

# EO
target_image = shots[target_name]
rotation = target_image["rotation"]
translation = target_image["translation"]
gps_position = target_image["gps_position"]

# IO
camera = target_image["camera"]
width, height = cameras[camera]["width"], cameras[camera]["height"]   # px
# Computing focal length - https://github.com/mapillary/OpenSfM/issues/84
focal_length = cameras[camera]["focal"] * np.max([width, height])     # px

# GP
df = pd.read_csv(fname2, skiprows=1, sep='\t+', header=None)
df.columns = ["image", "track_id", "feature_id", "feature_x", "feature_y", "feature_z", "r", "g", "b", "segmentation", "instance"]
## extract track_id
tracks_id = df.loc[df['image'] == target_name]["track_id"]
## query points by track_id in target_image(03.jpg)
tmp = []
for key in tracks_id:
    row = points.get(str(key))
    if row is None:
        continue
    color, coordinates = row["color"], row["coordinates"]
    # id, r, g, b, x, y, z
    tmp.append([key, coordinates[0], coordinates[1], coordinates[2], color[0], color[1], color[2]])
new_points = np.array(tmp)
print(new_points)

# Generate new reconstruction.json 
# Keep: cameras, biases, reference_lla
# Edit: shots, points
shots.pop("01.jpg", None)
shots.pop("02.jpg", None)
unwanted = set(points) - set(new_points[:, 0].astype(int).astype(str))
for unwanted_key in unwanted:
    del points[unwanted_key]

with open(fname3, 'w') as f:
    json.dump([data], f)

print("Bye")