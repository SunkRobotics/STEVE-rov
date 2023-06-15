rm -rf reconstruction/*
python MvgMvsPipeline.py images reconstruction
openMVG-bin/openMVG_main_openMVG2openMVS -i reconstruction/sfm/sfm_data.bin -o scene.mvs -d scene_undistorted && openMVS-bin/DensifyPointCloud scene.mvs && openMVS-bin/Viewer scene_dense.mvs
