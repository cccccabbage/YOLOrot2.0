import cv2
import math
import os
import glob
from pathlib import Path
import numpy as np

img_formats = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']


def getContours(img, cThr=[100,100], showCanny=False, minArea=1000, filter=0, draw =False):
    """获取长方形物体的轮廓，以及按照左上 -> 右上 -> 左下 -> 右下顺序排列的轮廓的四个角点"""
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 3)
    imgBlur = cv2.medianBlur(imgGray, 7)

    # 转化为二值图像
    ret, binary = cv2.threshold(imgBlur, 120, 255, cv2.THRESH_BINARY)
    imgCanny = cv2.Canny(binary, cThr[0], cThr[1])
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=3)  # 膨胀
    imgThre = cv2.erode(imgDial, kernel, iterations=2)  # 腐蚀

    if showCanny:
        cv2.imshow('Canny', imgThre)
    contours, hiearchy = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finalCountours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i,True)  # 获取轮廓参数
            approx = cv2.approxPolyDP(i, 0.02*peri, True)  # 获取轮廓的四个角点
            bbox = cv2.boundingRect(approx)  # 给物体添加 bounding box
            if filter > 0:
                if len(approx) == filter:
                    finalCountours.append([len(approx), area, approx, bbox, i])
            else:
                finalCountours.append([len(approx), area, approx, bbox, i])
    finalCountours = sorted(finalCountours, key=lambda x: x[1], reverse=True)  # 将四个角点按照左上 -> 右上 -> 左下 -> 右下顺序排列
    if draw:  # 画出轮廓
        for con in finalCountours:
            cv2.drawContours(img, con[4], -1, (0, 0, 255), 3)

    return img, finalCountours


def reorder(myPoints):
    """由于获取轮廓的角点时是乱序获取的，因此需要将其按照左上 -> 右上 -> 左下 -> 右下的顺序排列"""
    myPointsNew = np.zeros_like(myPoints)
    myPoints = myPoints.reshape((4, 2))
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]  # 左上
    myPointsNew[3] = myPoints[np.argmax(add)]  # 右下
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]  # 右上
    myPointsNew[2] = myPoints[np.argmax(diff)]  # 左下
    return myPointsNew


def findDis(pts1, pts2):
    """推算A4纸上的长方形物体的长和宽"""
    return ((pts2[0] - pts1[0])**2 + (pts2[1] - pts1[1])**2)**0.5


def count_pixel(image_path):
    image = cv2.imread(image_path)  # 读取图片
    imgContour, contours =getContours(image,minArea=50000, filter=4,draw =False)
    if len(contours) != 0:
        biggest = contours[0][2]  # 获取A4纸轮廓的四个角点
        # 将A4纸中的长方形物体的四个角点，按照：左上 -> 右上 -> 左下 -> 右下 的顺序排列
        newPoints = reorder(biggest)
        # 推算A4纸中的长方形物体的长和宽
        newWidth_1 = round((findDis(newPoints[0][0] , newPoints[1][0]) ), 1)
        newHeight_1 = round((findDis(newPoints[0][0], newPoints[2][0]) ), 1)
        newWidth_2 = round((findDis(newPoints[2][0], newPoints[3][0]) ), 1)
        newHeight_2 = round((findDis(newPoints[1][0], newPoints[3][0]) ), 1)

        cv2.line(image, tuple(newPoints[0][0]), tuple(newPoints[1][0]), (0, 255, 0), 2)
        cv2.line(image, tuple(newPoints[0][0]), tuple(newPoints[2][0]),(0, 255, 0), 2)
        cv2.line(image, tuple(newPoints[2][0]), tuple(newPoints[3][0]), (0, 255, 0), 2)
        cv2.line(image, tuple(newPoints[1][0]), tuple(newPoints[3][0]), (0, 255, 0), 2)

        if newWidth_1 <1000 or newHeight_1<1000 or newWidth_2<1000 or newHeight_2<1000:
            pixel=0
        else:
            pixel=(210+279)*2/(newWidth_1+newHeight_1+newWidth_2+newHeight_2)
    else:
        pixel =0
    if pixel==0:
        print('11111111111111111111111')
        print(image_path)
        print('33333333333333333333333')
    return round(pixel, 6)


if __name__ == '__main__':
    source = './'
    p = str(Path(source).absolute())
    files = glob.glob(os.path.join(p, '*.*'))  # dir
    images = [x for x in files if x.split('.')[-1].lower() in img_formats]
    # print(images)
    for i, imgpath in enumerate(images):
        px = count_pixel(imgpath)
        print(px)
