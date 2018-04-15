
# functions for doing NSynth encoding manipulations
import os
import numpy as np

def horhr():
    print("here")

def swapper(ipath, opath, file1, file2, SC, selective):
    print("here")
    enc1 = np.load(os.path.join(ipath,file1))
    enc2 = np.load(os.path.join(ipath,file2))
    file1 = file1.replace(".npy","")
    file2 = file2.replace(".npy","")
    

    
    num_swaps = 1
    if(not selective):
        num_swaps = 16
    
    for c in range(num_swaps):
        
        # duplicate encodings
        A = np.array(enc1)
        B = np.array(enc2)
        
        # swap channels
        for i in range(len(enc1[0])):
            for j in range(16):
                if(SC[j]==1 and selective):
                    A[0][i][j] = enc2[0][i][j]
                    B[0][i][j] = enc1[0][i][j]
                    
                if(j==c and not selective):
                    A[0][i][j] = enc2[0][i][j]
                    B[0][i][j] = enc1[0][i][j]
        
        # name encodings with swapped channels
        swapAname = file1+"-"+file2+"-"
        swapBname = file2+"-"+file1+"-"
        for i in range(16):
            if(not selective):
                if(i==c):
                    swapAname += "1"
                    swapBname += "1"
                else:
                    swapAname += "0"
                    swapBname += "0"
            else:
                swapAname += str(SC[i])
                swapBname += str(SC[i])
                
        # save encodings with swapped channels
        np.save(os.path.join(opath,"swap_"+swapAname+".npy"), A)
        np.save(os.path.join(opath,"swap_"+swapBname+".npy"), B)


def mixer(SC, ipath, opath, file1, file2):
    
    enc1 = np.load(os.path.join(ipath,file1))
    enc2 = np.load(os.path.join(ipath,file2))
    file1 = file1.replace(".npy","")
    file2 = file2.replace(".npy","")
       
    # duplicate encodings
    A = np.array(enc1)
    B = np.array(enc2)
    
    # swap channels
    for i in range(len(enc1[0])):
        for j in range(16):
            if(SC[j] > 0.0):
                A[0][i][j] = enc2[0][i][j]*SC[j] + enc1[0][i][j]*(1.0-SC[j])
                B[0][i][j] = enc1[0][i][j]*SC[j] + enc2[0][i][j]*(1.0-SC[j])
        
    # name encodings with swapped channels
    swapAname = file1+"-"+file2+"-"
    swapBname = file2+"-"+file1+"-"
    for i in range(16):
        swapAname += str(SC[i])
        swapBname += str(SC[i])
        if i < 15:
            swapAname += "_"
            swapBname += "_"
                
    # save encodings with swapped channels
    np.save(os.path.join(opath,"swap_"+swapAname+".npy"), A)
    np.save(os.path.join(opath,"swap_"+swapBname+".npy"), B)



