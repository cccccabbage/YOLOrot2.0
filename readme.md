## YOLOrot2.0
YOLOrot2.0 is a specialized algorithm for detecting rotated objects, with a specific focus on small objects like rice seeds. It includes a real-size measurement algorithm that allows for the conversion of pixel length and height into real-world measurement units. The rotated object detection algorithm employs a combination of SPDConv, RCS-OSA, and KFIoU loss to optimize performance in detecting small objects as well as rotated objects. Additionally, an online application is provided to enhance the usability of YOLOrot2.0 👉[here](http://www.xhhuanglab.cn/tool/SeedRuler.html).


## Dataset
Experiments were conducted on the [this dataset](https://www.kaggle.com/datasets/cccccabbage/rice370), which consists of 371 rice seed images of total 40,000 seeds.
The images contain the targets, plump rice seeds, and distruction like shriveled seeds and stems. Each image contains 50-150 seeds on average.
About 80% of seed images are labeled manually for trainning and evaluating.

## Environment and usage

### requirements
The requirements are almost the same as the [ultralytics](https://github.com/ultralytics/ultralytics), and a requirements.txt is also provided if needed.
```
pip install ultralytics
# or pip install -r requirements.txt
```

### dataset
The dataset can be found [here](https://www.kaggle.com/datasets/cccccabbage/rice370).

The dataset directory should be formatted as follow:
```
YOLOrot2.0
|   dataset
|   |   images
|   |   |   train
|   |   |   |   1.jpg
|   |   |   |   ......
|   |   |   test
|   |   |   val
|   |   labels
|   |   |   train
|   |   |   |   1.txt
|   |   |   |   ......
|   |   |   test
|   |   |   val
|   |   rice370.yaml
```

### train
```
cd YOLOrot2.0
python train.py
```

### test
```
cd YOLOrot2.0
# remember to edit the weight path in test.py
python test.py
```
