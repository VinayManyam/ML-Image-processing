import cv2
import numpy as np


src = cv2.imread("wfc1.jpg", cv2.IMREAD_GRAYSCALE)
needle = cv2.imread("way.jpg", 0)
threshold = 0.8
gsrc = cv2.cuda_GpuMat()
gtmpl = cv2.cuda_GpuMat()
gresult = cv2.cuda_GpuMat()
gsrc.upload(src)
gtmpl.upload(needle)
match_time = time.time()
matcher = cv2.cuda.createTemplateMatching(cv2.CV_8UC1, cv2.TM_CCOEFF_NORMED)
gresult = matcher.match(gsrc, gtmpl)
result_time = time.time()
resultg = gresult.download()
w, h = needle.shape[::-1]
loc = np.where( resultg >= threshold)
if not loc[1].size==0:
    for pt in zip(*loc[::-1]):
        cv2.rectangle(src, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        print("Match Found :")
        cv2.imwrite("final1.jpg",src)
        break   