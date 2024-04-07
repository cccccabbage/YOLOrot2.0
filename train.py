from ultralytics import YOLO
import gc

def oneTrainingTask(cfgPath, kfFlag, data="dataset/rice370.yaml"):
    model = YOLO(
        cfgPath,
        task="obb",
    )
    model.train(
        data=data,
        epochs=300,
        imgsz=640,
        batch=4,
        workers=8,
        use_kfiou=kfFlag,
        half=False,
        amp=False,
    )
    del model
    gc.collect()


def main():
    oneTrainingTask("ultralytics/cfg/models/v8/yolov8s-RCSOSA-SPDConv-obb.yaml", True)


if __name__ == "__main__":
    main()