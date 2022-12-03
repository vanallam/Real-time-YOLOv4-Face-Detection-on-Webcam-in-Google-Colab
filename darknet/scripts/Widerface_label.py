import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets=[("wider_face_val_bbx_gt")]

classes = ["face"]


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    image_id1 = image_id.split("/")
    image_id1 = image_id1[1]
    in_file = open('/content/WIDER_val_annotations/%s'%(image_id1.replace('.jpg','.xml')))
    out_file = open('/content/WIDER_val/images/%s.txt'%(image_id).replace('.jpg',''), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    #size = W*h

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = 0
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

for image_set in sets:
  

  list_file = open('%s.txt'%(image_set), 'w')
  with open('/content/wider_face_split/%s.txt'%(image_set)) as f:
    x = 0
    while x < 3300:
        x = x + 1
      image_id = f.readline().strip() 
      if image_id:
        list_file.write('/content/WIDER_val/images/%s\n'%(image_id))
        convert_annotation(image_id)
        nbBndboxes = f.readline()
        i = 0
        while i < int(nbBndboxes):
          i = i + 1
          f.readline().split()

    list_file.close()


