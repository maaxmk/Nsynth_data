import numpy
import os

def swapper(ipath, opath, file1, file2, SC = numpy.zeros(16), selective = True, output_invert=True):
    
    enc1 = numpy.load(os.path.join(ipath,file1))
    enc2 = numpy.load(os.path.join(ipath,file2))
    file1 = file1.replace(".npy","")
    file2 = file2.replace(".npy","")


    num_swaps = 1
    if(not selective):
        num_swaps = 16
    
    for c in range(num_swaps):
        
        # duplicate encodings
        A = numpy.array(enc1)
        B = numpy.array(enc2)
        
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
        swapAname = file1+"-"+file2+"_"
        swapBname = file2+"-"+file1+"_"
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
        numpy.save(os.path.join(opath,"swap_"+swapAname+".npy"), A)
        if(output_invert):
            numpy.save(os.path.join(opath,"swap_"+swapBname+".npy"), B)


def mixer(CM, ipath, opath, file1, file2, output_invert=True):
    
    enc1 = numpy.load(os.path.join(ipath,file1))
    enc2 = numpy.load(os.path.join(ipath,file2))
    file1 = file1.replace(".npy","")
    file2 = file2.replace(".npy","")
       
    # duplicate encodings
    A = numpy.array(enc1)
    B = numpy.array(enc2)
    
    # swap channels
    for i in range(len(enc1[0])):
        for j in range(16):
            if(CM[j] > 0.0):
                A[0][i][j] = enc2[0][i][j]*CM[j] + enc1[0][i][j]*(1.0-CM[j])
                B[0][i][j] = enc1[0][i][j]*CM[j] + enc2[0][i][j]*(1.0-CM[j])
        
    # name encodings with swapped channels
    swapAname = file1+"-"+file2+"_"
    swapBname = file2+"-"+file1+"_"
    for i in range(16):
        swapAname += "%.3f" % CM[i]
        swapBname += "%.3f" % CM[i]
        if i < 15:
            swapAname += "_"
            swapBname += "_"
                
    # save encodings with swapped channels
    numpy.save(os.path.join(opath,"mix_"+swapAname+".npy"), A)
    if(output_invert):
        numpy.save(os.path.join(opath,"mix_"+swapBname+".npy"), B)


def gain(CG, ipath, opath, file):

    enc = numpy.load(os.path.join(ipath,file))
    file = file.replace(".npy","")

    # apply gain to channels
    for i in range(len(enc[0])):
        for j in range(16):
            enc[0][i][j] = enc[0][i][j]*CG[j]

    swapName = file+"_"
    for i in range(16):
        swapName += "%.3f" % CG[i]
        if i < 15:
            swapName += "_"
                
    # save encodings with channel gain changes 
    numpy.save(os.path.join(opath,"gain_"+swapName+".npy"), enc)





