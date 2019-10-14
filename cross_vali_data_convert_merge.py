import numpy as np,numpy
import csv
import glob
import os

window_size = 100
threshold = 6
slide_size = 20 #less than window_size!!!

###
object_size = 5
current_csv_name = ""
current_category = ""
csv_category = ["bed", "fall", "pickup", "run", "sitdown", "standup", "walk"]
csv_category_filenames = list()
same_category_csv_count = 0
####



# def dataGrouping(path1, path2):
    # current_csv_name = ""
    # input_csv_files = sorted(glob.glob(path1))
    # for f in input_csv_files:
        # current_csv_name = os.path.basename(f)
        # for idx,cat in enumerate(csv_category):
            # #print("cat:",cat)
            # if "run" in current_csv_name:
                # print("cat:",cat)
            # print(current_csv_name)

            # if cat in current_csv_name:
                # temp_name = "csv_"+cat
                # if temp_name not in locals():
                    # exec("%s = list()" % (temp_name))
                    # print("new list created, ",temp_name)
                # else:
                    # exec("csv_%s.append(%s)"%(cat,"current_csv_name"))

                # print("csv_"+cat)
                # #exec("print(csv_bed)")
               # #exec("print(csv_run)")

    # print("end")

def dataimport(path1, path2):
    current_csv_name = ""
    # current_category = csv_category[0]
    # same_category_csv_count = 0
    xx = np.empty([0,window_size,90],float)
    yy = np.empty([0,8],float)

    ###Input data###
    #data import from csv
    input_csv_files = sorted(glob.glob(path1))
    object_count = 0
    for f in input_csv_files:
        current_csv_name = os.path.basename(f)
            # print("current_csv_name:", current_csv_name)
            # if current_category in current_csv_name:
                # same_category_csv_count+=1

        #print("processing input_file_name=",current_csv_name,"...")
        print("processing ",current_csv_name,"...")
        data = [[ float(elm) for elm in v] for v in csv.reader(open(f, "r"))]
        tmp1 = np.array(data)
        x2 =np.empty([0,window_size,90],float)

        #data import by slide window
        k = 0
        while k <= (len(tmp1) + 1 - 2 * window_size):
            x = np.dstack(np.array(tmp1[k:k+window_size, 1:91]).T)
            x2 = np.concatenate((x2, x),axis=0)
            k += slide_size
            if k%1000 == 0:
                print("k:",k)

        xx = np.concatenate((xx,x2),axis=0)
        object_count+=1
        if object_count >=object_size:
            break
    xx = xx.reshape(len(xx),-1)

        ###Annotation data###
        #data import from csv
    annotation_csv_files = sorted(glob.glob(path2))
    for ff in annotation_csv_files:
        print("annotation_file_name=",ff)
        ano_data = [[ str(elm) for elm in v] for v in csv.reader(open(ff,"r"))]
        tmp2 = np.array(ano_data)

        #data import by slide window
        y = np.zeros(((len(tmp2) + 1 - 2 * window_size)//slide_size+1,8))
        k = 0
        while k <= (len(tmp2) + 1 - 2 * window_size):
            y_pre = np.stack(np.array(tmp2[k:k+window_size]))
            bed = 0
            fall = 0
            walk = 0
            pickup = 0
            run = 0
            sitdown = 0
            standup = 0
            noactivity = 0
            for j in range(window_size):
                if y_pre[j] == "bed":
                    bed += 1
                elif y_pre[j] == "fall":
                    fall += 1
                elif y_pre[j] == "walk":
                    walk += 1
                elif y_pre[j] == "pickup":
                    pickup += 1
                elif y_pre[j] == "run":
                    run += 1
                elif y_pre[j] == "sitdown":
                    sitdown += 1
                elif y_pre[j] == "standup":
                    standup += 1
                else:
                    noactivity += 1

            if k%5000 ==0:
                print("k:",k)
                if len(y >0):
                    print("y[0]:",y[0])
                if len(y_pre) >0:
                    print("y_pre[0]:",y_pre[0])



            if bed > window_size * threshold / 100:
                y[int(k/slide_size),:] = np.array([0,1,0,0,0,0,0,0])
            elif fall > window_size * threshold / 100:
                y[int(k/slide_size),:] = np.array([0,0,1,0,0,0,0,0])
            elif walk > window_size * threshold / 100:
                y[int(k/slide_size),:] = np.array([0,0,0,1,0,0,0,0])
            elif pickup > window_size * threshold / 100:
                y[int(k/slide_size),:] = np.array([0,0,0,0,1,0,0,0])
            elif run > window_size * threshold / 100:
                y[int(k/slide_size),:] = np.array([0,0,0,0,0,1,0,0])
            elif sitdown > window_size * threshold / 100:
                y[int(k/slide_size),:] = np.array([0,0,0,0,0,0,1,0])
            elif standup > window_size * threshold / 100:
                y[int(k/slide_size),:] = np.array([0,0,0,0,0,0,0,1])
            else:
                # if k==0:
                    # y[k/slide_size] = np.array([2,0,0,0,0,0,0,0])
                # else:
                y[int(k/slide_size),:] = np.array([2,0,0,0,0,0,0,0])
            k += slide_size

        yy = np.concatenate((yy, y),axis=0)
    print(xx.shape,yy.shape)
    return (xx, yy)


#### Main ####
print("object_size by KHJ : ",object_size)
if not os.path.exists("input_files/"):
        os.makedirs("input_files/")

for i, label in enumerate (["bed", "fall", "pickup", "run", "sitdown", "standup", "walk"]):
        filepath1 = "./Dataset/Data/input_*" + str(label) + "*.csv"
        filepath2 = "./Dataset/Data/annotation_*" + str(label) + "*.csv"
        outputfilename1 = "./input_files/xx_" + str(window_size) + "_" + str(threshold) + "_" + label + ".csv"
        outputfilename2 = "./input_files/yy_" + str(window_size) + "_" + str(threshold) + "_" + label + ".csv"

        #dataGrouping(filepath1,filepath2)
        x, y = dataimport(filepath1, filepath2)
        with open(outputfilename1, "w") as f:
                writer = csv.writer(f, lineterminator="\n")
                writer.writerows(x)
        with open(outputfilename2, "w") as f:
                writer = csv.writer(f, lineterminator="\n")
                writer.writerows(y)
        print(label + "finish!")
