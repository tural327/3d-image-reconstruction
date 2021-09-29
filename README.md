<p align="center">
   3D Image-Reconstruction
 </p>
<p align="center">
    <img src="https://github.com/tural327/3d-image-reconstruction/blob/main/intro.png"/>
</p>

# Software
- App developed Ubuntu 20.04 
- Python 3.8 
**Python libraries I uesd**
- Pyqt5
- cv2
- numpy
- pickle
- matplotlib

## 1. Camera calibration ##

For calibrationg camera I used [Opencv module](https://docs.opencv.org/3.4.15/dc/dbb/tutorial_py_calibration.html)  for calibrate my camera. Itook several **CHECKERBOARD**images using my notebook camera and saved my camera matrix such as : [distortion](https://github.com/tural327/3d-image-reconstruction/blob/main/distortion.npy),[matrix](https://github.com/tural327/3d-image-reconstruction/blob/main/matrix.npy),[t_vecs](https://github.com/tural327/3d-image-reconstruction/blob/main/t_vecs.npy)
## 2. Finding EssentialMatrix ##
Parametrs which we got by doing calibration loaded [my3d](https://github.com/tural327/3d-image-reconstruction/blob/main/my3d.py) file for second step images for making 3d reconstruction we need find image matching keypoints points for that I used cv2.ORB_create()
```python
    orb = cv2.ORB_create()
    kp_sh1, descpirt1 = orb.detectAndCompute(img1,None)
    kp_sh2, descpirt2 = orb.detectAndCompute(img2,None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck = None)
    matches = bf.match(descpirt1,descpirt2)
    matches = sorted(matches,key= lambda x:x.distance)
 ```
Result was:

<p align="center">
    <img src="https://github.com/tural327/3d-image-reconstruction/blob/main/keypoints.png"/>
</p>

for next we need get mathced keypoints values

for that reason I used code selected each matched point of images:
```python
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
 ```

for second part our mission was making input for EssentialMatrix 
```python
    cord1 = np.zeros((len(list_kp1),1,2), dtype=np.float32) # format of input
    cord2 = np.zeros((len(list_kp2),1,2), dtype=np.float32)

    for i in list_kp1:
        my_cord = list(i)
        index_value = list_kp1.index(i)
        cord1[index_value][0] = my_cord

    for j in list_kp2:
        my_cord2 = list(j)
        index_value2 = list_kp2.index(j)
        cord2[index_value2][0] = my_cord2
 ```
 after finding cord1 and cord2 arrays I converted it to undistortPoints now we can get our EssentialMatrix
 ```python
 E, mask = cv2.findEssentialMat(xy_undistorted1,xy_undistorted2,matrix,method=None,prob=None,threshold=None,maxIters=None,mask=None)
  ```
 Next find camre Rotation and Translation 
  ```python
 points, R_est, t_est, mask_pose = cv2.recoverPose(E,xy_undistorted1,xy_undistorted2)
  ```
