import os

path = "images/out/"
dir = os.listdir(path)

for file in dir:
    if file[0:5] == "APPLE":
        target = file.find('target')
        if target == -1:
            continue
        actual = file.find('actual')
        newName = "APPLE_t"+file[target+6:target+11]+"_a"+file[actual+6:actual+12]+'_'+file[-7:]
        os.rename(path+file, path+newName)

    if file[0:4] == "ARRI":
        target = file.find('target')
        if target == -1:
            continue
        actual = file.find('actual')
        newName = "ARRI_t"+file[target+6:target+11]+"_a"+file[actual+6:actual+12]+'_'+file[-7:]
        os.rename(path+file, path+newName)

    if file[0:4] == "bike":
        target = file.find('target')
        if target == -1:
            continue
        actual = file.find('actual')
        newName = "bike_t" + file[target + 6:target + 11] + "_a" +file[actual+6:actual+12]+'_'+file[-7:]
        os.rename(path + file, path + newName)

    if file[0:4] == "cafe":
        target = file.find('target')
        if target == -1:
            continue
        actual = file.find('actual')
        newName = "cafe_t"+file[target+6:target+11]+"_a"+file[actual+6:actual+12]+'_'+file[-7:]
        os.rename(path + file, path + newName)

    if file[0:8] == "horsefly":
        target = file.find('target')
        if target == -1:
            continue
        actual = file.find('actual')
        newName = "horsefly_t"+file[target+6:target+11]+"_a"+file[actual+6:actual+12]+'_'+file[-7:]
        os.rename(path + file, path + newName)

    if file[0:3] == "p06":
        target = file.find('target')
        if target == -1:
            continue
        actual = file.find('actual')
        newName = "p06_t"+file[target+6:target+11]+"_a"+file[actual+6:actual+12]+'_'+file[-7:]
        os.rename(path + file, path + newName)

    if file[0:7] == "Sintel2":
        target = file.find('target')
        if target == -1:
            continue
        actual = file.find('actual')
        newName = "Sintel2_t"+file[target+6:target+11]+"_a"+file[actual+6:actual+12]+'_'+file[-7:]
        os.rename(path + file, path + newName)