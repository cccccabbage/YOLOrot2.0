from ultralytics import YOLO

def main():
    weightPath = "There should be a path to a trained weight file here."
    # weightPath = "runs/obb/train/weights/best.pt" # make sure this is a trained weight file

    model = YOLO(weightPath)
    model.predict(
        "testImgs",
        save=True,
        conf=0.7,
        line_width=1,
        visualize=False,
    )


if __name__ == "__main__":
    main()