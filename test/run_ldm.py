import queue
from re import sub
import subprocess
import os
import shutil
import sys

sys.path.insert(0, '/source/OpenSfM')   # Now can import modules in built in /source/opensfm
from opensfm.actions import export_geocoords2
from opensfm.dataset import DataSet

root = '/source/OpenSfM'
exec = os.path.join(root, 'bin/opensfm')
data_path = os.path.join(root, 'data/yangpyeong')

# Reset results
datas = os.listdir(data_path)
for data in datas:
    path = os.path.join(data_path, data)
    if not (data in ['images', 'queue', 'config.yaml']):
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)

proj = '+proj=tmerc +lat_0=38 +lon_0=127 +k=1 +x_0=200000 +y_0=600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'

queue_files = os.listdir(os.path.join(data_path, 'queue'))
queue_files.sort()
for i in range(len(queue_files) + 1):
    print(f'{i} th run')
    if i == 0:        
        subprocess.run([exec, 'extract_metadata', data_path])
        subprocess.run([exec, 'detect_features', data_path])
        subprocess.run([exec, 'match_features', data_path])
        subprocess.run([exec, 'create_tracks', data_path])
        subprocess.run([exec, 'reconstruct', data_path])
        subprocess.run([exec, 'export_geocoords', '--proj', proj, '--transformation', data_path])
        subprocess.run([exec, 'export_geocoords', '--proj', proj, '--image-positions', data_path])
        subprocess.run([exec, 'export_geocoords', '--proj', proj, '--reconstruction', data_path])
        # TODO: Select points by an image
        # # Query points by track_id in target_image
        # from opendm.ldm.points import query_points
        # query_points(tree.opensfm_reconstruction, octx.path('tracks.csv'), tree.dataset_list, octx.path('reconstruction_org.json'))
        subprocess.run([exec, 'export_ply', '--no-cameras', data_path])
        
        ids, eos, pts = export_geocoords2.run_dataset(data=DataSet(data_path), proj=proj,
                                                      transformation=False, image_positions=False, reconstruction=False, dense=False,
                                                      georef=True, output=data_path)
        # TODO: Visualize the intermediate result
    else:
        # Move new image from 'queue' foler to 'images' folder
        subprocess.run(['cp', os.path.join(data_path, 'queue', queue_files[i - 1]), os.path.join(data_path, 'images', queue_files[i - 1])])
        subprocess.run([exec, 'extract_metadata', data_path])
        subprocess.run([exec, 'detect_features', data_path])
        subprocess.run([exec, 'match_features', data_path])
        subprocess.run([exec, 'create_tracks', data_path])
        subprocess.run([exec, 'reconstruct_from_prior', data_path]) # TODO: Check the region
        subprocess.run([exec, 'export_geocoords', '--proj', proj, '--transformation', data_path])
        subprocess.run([exec, 'export_geocoords', '--proj', proj, '--image-positions', data_path])
        # TODO: Select points by an image
        subprocess.run([exec, 'export_ply', '--no-cameras', data_path])
    
# Restore an original state
images = os.listdir(os.path.join(data_path, 'images'))
for image in images:
    if image in queue_files:
        os.remove(image)


# # 1. extract_metadata
# print(f"\n\n********************\n* extract_metadata *\n********************")
# subprocess.run([exec, 'extract_metadata', data_path])
# # 2. detect_features
# print(f"\n\n*******************\n* detect_features *\n*******************")
# subprocess.run([exec, 'detect_features', data_path])
# # 3. match_features
# print(f"\n\n******************\n* match_features *\n******************")
# subprocess.run([exec, 'match_features', data_path])
# # 4. create_tracks
# print(f"\n\n*****************\n* create_tracks *\n*****************")
# subprocess.run([exec, 'create_tracks', data_path])
# # 5. reconstruct
# print(f"\n\n***************\n* reconstruct *\n***************")
# subprocess.run([exec, 'reconstruct', data_path])
# # 6. export_geocoords ... TODO: How can I export EOP(X, Y, Z, O, P, K)??
# # --transformation: geocoords_transformation.txt
# # --image-positions: image_geocoords.tsv
# # --reconstruction: reconstruction.geocoords.json
# # --output
# print(f"\n\n********************\n* export_geocoords *\n********************")
# subprocess.run([exec, 'export_geocoords', '--proj', proj, '--reconstruction', data_path])
# #subprocess.run([exec, 'export_geocoords', '--proj', proj, '--image-positions' data_path])
# # 7. TODO: Override exif - exif_overrides.json in data_path
# # example:
# # {
# #     "image_name.jpg": {
# #         "gps": {
# #             "latitude": 52.51891,
# #             "longitude": 13.40029,
# #             "altitude": 27.0,
# #             "dop": 5.0
# #         }
# #     }
# # }
# # should replace data["image_name.jpg"]["gps"]["latitude"] to computed latitude