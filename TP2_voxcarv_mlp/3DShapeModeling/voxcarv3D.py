import math as m
import matplotlib.image as mpimg
import numpy as np
import skimage
from skimage import measure
# import torch
# from torch import nn
import trimesh


# Camera Calibration for Al's image[1..12].pgm   
calib=np.array([[-230.924, 0, -33.6163, 300,  -78.8596, -178.763, -127.597, 300,  -0.525731, 0, -0.85065, 2],
[-178.763, -127.597, -78.8596, 300,  0, -221.578, 73.2053, 300,  0, -0.85065, -0.525731, 2],
[-73.2053, 0, -221.578, 300,  78.8596, -178.763, -127.597, 300,  0.525731, 0, -0.85065, 2],
[-178.763, 127.597, -78.8596, 300,  0, 33.6163, -230.924, 300,  0, 0.85065, -0.525731, 2],
[73.2053, 0, 221.578, 300,  -78.8596, -178.763, 127.597, 300,  -0.525731, 0, 0.85065, 2],
[230.924, 0, 33.6163, 300,  78.8596, -178.763, 127.597, 300,  0.525731, 0, 0.85065, 2],
[178.763, -127.597, 78.8596, 300,  0, -221.578, -73.2053, 300,  0, -0.85065, 0.525731, 2],
[178.763, 127.597, 78.8596, 300,  0, 33.6163, 230.924, 300,  0, 0.85065, 0.525731, 2],
[-127.597, -78.8596, 178.763, 300,  -33.6163, -230.924, 0, 300,  -0.85065, -0.525731, 0, 2],
[-127.597, 78.8596, 178.763, 300,  -221.578, -73.2053, 0, 300,  -0.85065, 0.525731, 0, 2],
[127.597, 78.8596, -178.763, 300,  221.578, -73.2053, 0, 300,  0.85065, 0.525731, 0, 2],
[127.597, -78.8596, -178.763, 300,  33.6163, -230.924, 0, 300,  0.85065, -0.525731, 0, 2]])


# Build 3D grids
resolution=300   # 3D Grids are of size: resolution x resolution x resolution/2
step = 2/resolution    
X, Y, Z = np.mgrid[-1:1:step, -1:1:step, -0.5:0.5:step]  # Voxel coordinates
occupancy = np.ndarray(shape=(resolution,resolution,int(resolution/2)), dtype=int) #Voxel occupancy
occupancy.fill(0) # Voxels are initially occupied then carved with silhouette information

def in_frame(coord, img):
    img_h = len(img)
    img_w = img.size / img_h
    return not(coord[0] < 0 or coord[0] >= img_w or coord[1] < 0 or coord[1] >= img_h)
        

####### MAIN #########  
if __name__ == "__main__":
    # Compute grid projection in images
    #TO BE COMPLETED
    num_img = 5
    
    images = []
    for c in range(12):
        myFile = "image{0}.pgm".format(c) # read the input silhouettes
        print(myFile)
        img = mpimg.imread(myFile)
        if img.dtype == np.float32: # if not integer
            img = (img * 255).astype(np.uint8)
    
        images.append(img)
            
    for i in range(resolution):
        for j in range(resolution):
            for k in range(int(resolution/2)):
                count = 0
                for c in range(num_img):
                    # use image c Todo
                    img = images[c]
            
                    matrix = calib[c].reshape([3,4])
                    coord = np.array([i,j,k,1])
                    result = matrix @ coord
                    if result[2] != 0:
                        pixel_coord = np.array([int(result[0]/result[2]), int(result[1]/result[2])])
                        #check inside image
                        #check inside shiloutte
                        if in_frame(pixel_coord, img) and img[pixel_coord[1]][pixel_coord[0]] != 0:
                            count+=1
                        else:
                            break
                            
                if count == num_img:
                    occupancy[i][j][k] = 1
            
    
    # Update grid occupancy
    #TO BE COMPLETED

    # Voxel visualization
    verts, faces, normals, values = measure.marching_cubes(occupancy, 0.25) # Marching cubes 
    surf_mesh = trimesh.Trimesh(verts, faces, validate=True) # Export in a standard file format 
    surf_mesh.export('alvoxels.off')
 
