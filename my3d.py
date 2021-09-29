import numpy as np
import cv2
from matplotlib import pyplot as plt

# func for resize image for make it more fast
def image_resize(img,scale_percent):

    width = int((img.shape[1] * scale_percent)/100)
    height = int((img.shape[0] * scale_percent) / 100)
    dim = (width,height)

    resized = cv2.resize(img,dim, interpolation=cv2.INTER_AREA)

    return resized


# Adding parametrs of camera
with open('matrix.npy', 'rb') as f:
    matrix = np.load(f)

with open('distortion.npy', 'rb') as g:
    distortion = np.load(g)

with open('r_vecs.npy', 'rb') as t:
    r_vecs = np.load(t)

with open('t_vecs.npy', 'rb') as k:
    t_vecs = np.load(k)
def my_3d_func(img1,img2):
    # Reading random images
    img1 = cv2.imread(img1)
    img2 = cv2.imread(img2)
    # resizeng images
    img1 = image_resize(img1,20)
    img2 = image_resize(img2,20)

    # change it to Gray scale
    img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

    ### Finding images corners

    orb = cv2.ORB_create()



    kp_sh1, descpirt1 = orb.detectAndCompute(img1,None)

    kp_sh2, descpirt2 = orb.detectAndCompute(img2,None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck = None)

    matches = bf.match(descpirt1,descpirt2)
    matches = sorted(matches,key= lambda x:x.distance)

    # list for matched points
    list_kp1 = []
    list_kp2 = []

    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        # Get the coordinates
        (x1, y1) = kp_sh1[img1_idx].pt
        (x2, y2) = kp_sh2[img2_idx].pt

        # Append to each list
        list_kp1.append((x1, y1))
        list_kp2.append((x2, y2))


    list_kp1 = [kp_sh1[mat.queryIdx].pt for mat in matches]
    list_kp2 = [kp_sh2[mat.trainIdx].pt for mat in matches]

    # making imput for findEssentialMat
    cord1 = np.zeros((len(list_kp1),1,2), dtype=np.float32)
    cord2 = np.zeros((len(list_kp2),1,2), dtype=np.float32)



    for i in list_kp1:
        my_cord = list(i)
        index_value = list_kp1.index(i)
        cord1[index_value][0] = my_cord

    for j in list_kp2:
        my_cord2 = list(j)
        index_value2 = list_kp2.index(j)
        cord2[index_value2][0] = my_cord2


    # Finding undistortPoints for each image
    xy_undistorted1 = cv2.undistortPoints(cord1, matrix, distortion)
    xy_undistorted2 = cv2.undistortPoints(cord2, matrix, distortion)

    E, mask = cv2.findEssentialMat(xy_undistorted1,xy_undistorted2,matrix,method=None,prob=None,threshold=None,maxIters=None,mask=None)

    F, mask = cv2.findFundamentalMat(xy_undistorted1,xy_undistorted2,cv2.RANSAC,1.0,0.98)

    points, R_est, t_est, mask_pose = cv2.recoverPose(E,xy_undistorted1,xy_undistorted2)

    rotation_mat = np.zeros(shape=(3, 3))
    R = cv2.Rodrigues(r_vecs[0], rotation_mat)[0]
    P1 = np.column_stack((np.matmul(matrix,R), t_vecs[0]))

    # P2 = K[R|t] by manual
    P2 = np.concatenate((np.dot(matrix,R_est),np.dot(matrix,t_est)), axis = 1)


    # Main homogen_points of images
    homogen_points = cv2.triangulatePoints(P1,P2,xy_undistorted1,xy_undistorted2)
    points_3d = homogen_points[:3, :].T

    X = []
    Y = []
    Z = []

    for i in range(points_3d.shape[0]):
        xp = points_3d[i][0]
        yp = points_3d[i][1]
        zp = points_3d[i][2]

        X.append(xp)
        Y.append(yp)
        Z.append(zp)

    return X,Y,Z


