import argparse
import os

if __name__ == '__main__':
    opensfm_run_all_path = '/source/OpenSfM/bin/opensfm_run_all'
    opensfm_path = '/source/OpenSfM/bin/opensfm'
    
    parser = argparse.ArgumentParser(description='command')    
    
    parser.add_argument('--run-all', type=str, help='run all command')
    parser.add_argument('--extract-metadata', type=str, help='run extract metadata')
    parser.add_argument('--detect-features', type=str, help='run detect features')
    parser.add_argument('--match-features', type=str, help='run match features')
    parser.add_argument('--create-tracks', type=str, help='run create tracks')
    parser.add_argument('--reconstruct', type=str, help='run reconstruct')
    parser.add_argument('--reconstruct-from-prior', type=str, help='run reconstruct from prior')
    parser.add_argument('dataset', type=str, help='a path of dataset')

    args = parser.parse_args()
    run_all = args.run_all
    extract_metadata = args.extract_metadata
    detect_features = args.detect_features
    match_features = args.match_features
    create_tracks = args.create_tracks
    reconstruct = args.reconstruct
    reconstruct_from_prior = args.reconstruct_from_prior
    dataset = args.dataset
    
    if run_all:
        command = opensfm_run_all_path + ' ' + dataset        
    elif extract_metadata:
        command = opensfm_path + ' extract_metadata ' + dataset
    elif detect_features:
        command = opensfm_path + ' detect_features ' + dataset
    elif match_features:
        command = opensfm_path + ' match_features ' + dataset
    elif create_tracks:
        command = opensfm_path + ' create_tracks ' + dataset
    elif reconstruct:
        command = opensfm_path + ' reconstruct ' + dataset
    elif reconstruct_from_prior:
        command = opensfm_path + ' reconstruct_from_prior ' + dataset
    else:
        print("\nNothing!!!")
    
    os.system(command)