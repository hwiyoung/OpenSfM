import subprocess
import os
import shutil
import sys
import time

sys.path.insert(0, '/source/OpenSfM')   # Now can import modules in built in /source/opensfm
from opensfm.actions import export_geocoords2
from opensfm.dataset import DataSet

root = '/source/OpenSfM'
exec = os.path.join(root, 'bin/opensfm')
data_path = os.path.join(root, 'data/yangpyeong')

proj = '+proj=tmerc +lat_0=38 +lon_0=127 +k=1 +x_0=200000 +y_0=600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'

queue_files = os.listdir(os.path.join(data_path, 'queue'))
queue_files.sort()

# Reset dataset
datas = os.listdir(data_path)
for data in datas:
    path = os.path.join(data_path, data)
    if not (data in ['images', 'queue', 'config.yaml']):
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)

images = os.listdir(os.path.join(data_path, 'images'))
for image in images:
    if image in queue_files:
        os.remove(os.path.join(data_path, 'images', image))

# Processing
for i in range(len(queue_files) + 1):
    print(f'   ============\n     {i} th run\n   ============')
    start_time = time.time()
    subprocess.run([exec, 'extract_metadata', data_path])
    metadata_time = time.time() - start_time
    tic = time.time()
    subprocess.run([exec, 'detect_features', data_path])
    detect_time = time.time() - tic
    tic = time.time()
    subprocess.run([exec, 'match_features', data_path])
    match_time = time.time() - tic
    tic = time.time()
    subprocess.run([exec, 'create_tracks', data_path])
    tracks_time = time.time() - tic
    tic = time.time()
    if i == 0:        
        subprocess.run([exec, 'reconstruct', data_path])    # incremental_reconstruction        
    else:        
        subprocess.run([exec, 'extend_reconstruction', '--input', os.path.join(data_path, 'reconstruction.json'), 
                        '--output', os.path.join(data_path, 'reconstruction.json'), data_path]) # growing
    reconstruct_time = time.time() - tic
    tic = time.time()

    # TODO: Select points by an image
    # # Query points by track_id in target_image
    # from opendm.ldm.points import query_points
    # query_points(tree.opensfm_reconstruction, octx.path('tracks.csv'), tree.dataset_list, octx.path('reconstruction_org.json'))
    
    ids, eos, pts = export_geocoords2.run_dataset(data=DataSet(data_path), proj=proj,
                                                  transformation=False, image_positions=False, reconstruction=False, dense=False,
                                                  georef=True, output=data_path)
    geocoords_time = time.time() - tic
    print(f'   **************************\n'
          f'     metadata: {metadata_time:.2f} sec\n'
          f'     detect: {detect_time:.2f} sec\n'
          f'     match: {match_time:.2f} sec\n'
          f'     tracks: {tracks_time:.2f} sec\n'
          f'     reconstruct: {reconstruct_time:.2f} sec\n'
          f'     geocoords: {geocoords_time:.2f} sec\n'
          f'     Elapsed time: {time.time() - start_time:.2f} sec\n'
          f'   **************************\n')
    
    # Move new image from 'queue' foler to 'images' folder
    subprocess.run(['cp', os.path.join(data_path, 'queue', queue_files[i]), os.path.join(data_path, 'images', queue_files[i])])
    # TODO: Visualize the intermediate result

# 7. TODO: Override exif - exif_overrides.json in data_path
# example:
# {
#     "image_name.jpg": {
#         "gps": {
#             "latitude": 52.51891,
#             "longitude": 13.40029,
#             "altitude": 27.0,
#             "dop": 5.0
#         }
#     }
# }
# should replace data["image_name.jpg"]["gps"]["latitude"] to computed latitude