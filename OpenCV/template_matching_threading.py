import pandas as pd
import numpy as np
import cv2 as cv
import time
import threading



def rotate_image(image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv.warpAffine(image, rot_mat, image.shape[1::-1], borderMode=cv.BORDER_CONSTANT,borderValue=(0,0,0))
        return result


file_loc = "Book1.xlsx"
df = pd.read_excel(file_loc,sheet_name='images', usecols="A")
mylist = ["dt1.jpg","dt2.jpg","ESO510.jpg","IC5332.jpg","Whirlpool.jpg","M58.png","M91.png"]
col = [0,45,90,135,180,225,270,315]    
for y in mylist:
    name = y.split(".")
    ny = cv.imread(y)
    for x in col: 
        nname = name[0]+"_"+str(x)+".jpg"
        res=rotate_image(ny,x)
        cv.imwrite(nname,res)


file1 = open("cols.txt", "a")  # append mode
file1.truncate(0)

def process(x,row,y,tres,mycol):
    if row in mycol:
       return 0 
    xtmp=x.split(".")
    file_name=xtmp[0]+"_"+str(y)+".jpg"
    template = cv.imread(file_name,0)
    w, h = template.shape[::-1]
    img = "dss4/"+row
    name = x.split(".")
    img1 = "res_"+name[0]+"_"+str(y)+"_"+row
    img_rgb = cv.imread(img)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)    
    if not loc[1].size==0:
        if row not in mycol:
            for pt in zip(*loc[::-1]):
                cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
                print("Match Found :"+img1)
                #cv.imwrite(img1,img_rgb)
                val = {x:1}
                file1.write(img1+"\n")
                mycol.append(row)
                mycol=list(set(mycol));
                #print(mycol)
                tres.append(val)
                break
    val = {x:0}
    tres.append(val)
            
            
    return 0        
            
            

threshold = 0.8
i=0
print(len(df))	
start_time = time.time()	

def process1(x):
    cols=[]
    for i in x:
        if list(i.values())[0] == 1:
            cols.append(list(i.keys())[0])
        
    return cols        
	
rows = []    
for index, row in df.iterrows():
            rows.append(row[0])
           
            
rows_final = [item for item in rows if not(pd.isnull(item)) == True]    
k = 1

mycol = []
while k < len(rows_final)-1:
  #print(k)
  #print(rows_final[k])
   
  nlist=[]
  nlist = mylist.copy()
  col = [0,45,90,135,180,225,270,315]  
  for z in range(0,100):
    zname = "t" + str(z) 
    aname = "a" + str(z)
    globals()[f"{aname}"]=[] 
    for y in col:
        try:
            if rows_final[k+z]  in mycol:
                break
        except IndexError:
                pass            

        
        for x in nlist:
            try:
                if rows_final[k+z]  in mycol:
                    break
            except IndexError:
                pass
            #print(str(k) +" z: "+ str(z) +" img: "+rows[k+z])
            try:
                if rows_final[k+z] not in mycol:
                    globals()[f"{zname}"] = threading.Thread(target=process, args=(x,rows_final[k+z],y,eval(aname),mycol))
                    eval(zname).start()
                #eval(zname).join()
            except IndexError:
                pass
            
  k += 100                
print("--- %s seconds ---" % (time.time() - start_time))   