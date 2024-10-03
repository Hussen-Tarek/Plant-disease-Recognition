import numpy as np
import os, cv2, shutil
import matplotlib.pyplot as plt

'''
Note:
###First Select the desired classes of tomatos and copy the folders to /Tomato directory###
'''
'''
Select 950 sample from each class(because of class imbalance)
#Train: 665 sample
#Validation: 180
#Test: 105
'''
DATA_PATH = "Tomato"
tomato_data = os.listdir(DATA_PATH)

#INFO
for disease_class in tomato_data:
    print(disease_class+":",
          len(os.listdir(os.path.join(DATA_PATH,disease_class)))," images","\n")

#SETUP DATA DIRECTORIES
sampled_data_path = "tomato_sampled"
try:
    os.mkdir(sampled_data_path)
except:
    pass

for disease_class in tomato_data:
    disease_dir = os.path.join(sampled_data_path, disease_class)
    try:
        os.mkdir(disease_dir)
    except:
        pass

#SETUP TRAIN/VAL/TEST DIRECTORIES
train_dir = 'train'
try:
    os.mkdir(train_dir)
except:
    pass

validation_dir = 'validation'
try:
    os.mkdir(validation_dir)
except:
    pass
test_dir = 'test'
try:
    os.mkdir(test_dir)
except:
    pass
#CLASSES FOR TRAIN/VAL/TEST DIRECTORIES
machinelearning_data_dirs = [train_dir, validation_dir, test_dir]
for disease_class in tomato_data:
    for data_dir in machinelearning_data_dirs:
        disease_dir = os.path.join(data_dir, disease_class)
        try:
            os.mkdir(disease_dir)
        except:
            pass

#SAMPLE 950 SAMPLE TO tomato_sampled
for disease_class in tomato_data:
    disease_classdata = os.listdir(os.path.join(DATA_PATH,disease_class))
    for sample in range(950):
        sample_img = disease_classdata[sample]
        src = os.path.join(os.path.join(DATA_PATH,disease_class), sample_img)
        dst = os.path.join(os.path.join(sampled_data_path,disease_class), sample_img)
        shutil.copyfile(src, dst)

#COPY SAMPLED DATA TO TRAIN/VAL/TEST DIRECTORIES
sampled_tomato_data = os.listdir(sampled_data_path)
print("TRAIN/VAL/TEST sampling")
for disease_class in sampled_tomato_data:
    disease_images = os.listdir(os.path.join(sampled_data_path,disease_class))
    train_images = disease_images[0:665]
    validation_images = disease_images[665:845]
    test_images = disease_images[845:]
    #print train images, test images and validation images
    print(disease_class,len(train_images),len(validation_images),len(test_images),"\n")

    for train_image in train_images:
        src = os.path.join(os.path.join(sampled_data_path, disease_class), train_image)
        dst = os.path.join(os.path.join(train_dir,disease_class), train_image)
        shutil.copyfile(src, dst)

    for validation_image in validation_images:
        src = os.path.join(os.path.join(sampled_data_path, disease_class), validation_image)
        dst = os.path.join(os.path.join(validation_dir,disease_class), validation_image)
        shutil.copyfile(src, dst)

    for test_image in test_images:
        src = os.path.join(os.path.join(sampled_data_path, disease_class), test_image)
        dst = os.path.join(os.path.join(test_dir,disease_class), test_image)
        shutil.copyfile(src, dst)
###
###Now you have training, validation and test set of 6 classes (5 diseases and 1 healthy)
###
