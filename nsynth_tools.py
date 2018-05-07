import numpy
import os

def swapper(ipath, opath, file1_full, file2_full, SC = numpy.zeros(16), selective = True, output_invert=True):
    
    enc1 = numpy.load(os.path.join(ipath,file1_full))
    enc2 = numpy.load(os.path.join(ipath,file2_full))


    name_split = file1_full.split("_")
    file1 = name_split[3].replace(".npy","")
    name_split = file2_full.split("_")
    file2 = name_split[3].replace(".npy","")

    prefix = name_split[0]+"_"+name_split[1]+"_"


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
        numpy.save(os.path.join(opath,prefix+"swap_"+swapAname+".npy"), A)
        if(output_invert):
            numpy.save(os.path.join(opath,prefix+"swap_"+swapBname+".npy"), B)


def mixer(CM, ipath, opath, file1_full, file2_full, output_invert=True):
    
    lerp = False
    if len(CM)==1:
        lerp = True
        val = CM[0]
        CM = numpy.full(16,val)


    enc1 = numpy.load(os.path.join(ipath,file1_full))
    enc2 = numpy.load(os.path.join(ipath,file2_full))
    name_split = file1_full.split("_")
    file1 = name_split[3].replace(".npy","")
    name_split = file2_full.split("_")
    file2 = name_split[3].replace(".npy","")
    prefix = name_split[0]+"_"+name_split[1]+"_"

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
    if lerp:
        swapAname += "%.3f" % CM[0]
        swapBname += "%.3f" % CM[0]
    else:
        for i in range(16):
            swapAname += "%.3f" % CM[i]
            swapBname += "%.3f" % CM[i]
            if i < 15:
                swapAname += "_"
                swapBname += "_"
                
    # save encodings with swapped channels
    if lerp:
        numpy.save(os.path.join(opath,prefix+"lerp_"+swapAname+".npy"), A)
        if output_invert:
            numpy.save(os.path.join(opath,prefix+"lerp_"+swapBname+".npy"), B)
    else:
        numpy.save(os.path.join(opath,prefix+"mix_"+swapAname+".npy"), A)
        if output_invert:
            numpy.save(os.path.join(opath,prefix+"mix_"+swapBname+".npy"), B)
    


def gain(CG, ipath, opath, file_full):

    enc = numpy.load(os.path.join(ipath,file_full))
    name_split = file_full.split("_")
    file = name_split[3].replace(".npy","")
    prefix = name_split[0]+"_"+name_split[1]+"_"

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
    numpy.save(os.path.join(opath,prefix+"gain_"+swapName+".npy"), enc)



def SH(file_full, ipath, opath, SHpos, SHlen, Insert=False, Lead=0):

    enc = numpy.load(os.path.join(ipath,file_full))
    name_split = file_full.split("_")
    file = name_split[3].replace(".npy","")
    newName = file+"_"+("%.3f" % SHpos)+"_"+str(Lead)+"_"+str(SHlen)
    prefix = name_split[0]+"_"+name_split[1]+"_"

    SHpos = int(round((len(enc[0])-1)*SHpos))

    A = numpy.zeros((1))

    if Insert:
        A = numpy.zeros((1,len(enc[0])+SHlen,16))

        for i in range(len(enc[0])):
            if i < SHpos:
                A[0][i] = enc[0][i]
            if i == SHpos:
                for j in range(SHlen+1):
                    A[0][SHpos+j] = enc[0][SHpos]
            if i > SHpos:
                A[0][i+SHlen] = enc[0][i]

    if not Insert:
        A = numpy.zeros((1,SHlen+Lead,16))

        for i in range(SHlen+Lead):

            if i < Lead:
                A[0][i] = enc[0][SHpos+i]
            else:
                A[0][i] = enc[0][SHpos+Lead]

    
    numpy.save(os.path.join(opath,prefix+"SH_"+newName+".npy"), A)



