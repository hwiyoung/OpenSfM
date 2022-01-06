import subprocess
from pathlib import Path


root = Path('/source/OpenSfM')
exec = root / 'bin/opensfm'
data_path = root / 'data/yangpyeong'

proj = '+proj=tmerc +lat_0=38 +lon_0=127 +k=1 +x_0=200000 +y_0=600000 +ellps=GRS80 +units=m +no_defs'

# 1. extract_metadata
print(f"\n\n********************\n* extract_metadata *\n********************")
subprocess.run([exec, 'extract_metadata', data_path])
# 2. detect_features
print(f"\n\n*******************\n* detect_features *\n*******************")
subprocess.run([exec, 'detect_features', data_path])
# 3. match_features
print(f"\n\n******************\n* match_features *\n******************")
subprocess.run([exec, 'match_features', data_path])
# 4. create_tracks
print(f"\n\n*****************\n* create_tracks *\n*****************")
subprocess.run([exec, 'create_tracks', data_path])
# 5. reconstruct
print(f"\n\n***************\n* reconstruct *\n***************")
subprocess.run([exec, 'reconstruct', data_path])
# 6. export_geocoords
# --transformation: geocoords_transformation.txt
# --image-positions: image_geocoords.tsv
# --reconstruction: reconstruction.geocoords.json
# --output
print(f"\n\n********************\n* export_geocoords *\n********************")
subprocess.run([exec, 'export_geocoords', '--proj', proj, '--reconstruction', data_path])
# 7. TODO: Override exif - exif_overrides.json in data_path