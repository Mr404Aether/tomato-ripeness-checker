# Tomato Ripeness Checker

A classical OpenCV desktop application that finds tomatoes in an image, a recorded video, or a live webcam feed and labels each one **NOT YET**, **ALMOST**, or **RIPE** from its color.

Made for CSC 126 (Computer Vision) midterm project.

**Team:** `[Member 1]`, `[Member 2]`, `[Member 3]`

## The problem

Home gardeners often cannot tell which tomatoes are ready to pick. Color is the most visible sign of ripeness, but judging it by eye is inconsistent. This application measures how much of each tomato is red, yellow-orange, or green and turns that into a label, so the answer does not depend on who is looking or on a guess.

## Features

- Finds **every** tomato in view (up to 12) and gives each one an ID (#1, #2, ...) that stays with it as it moves.
- Labels each tomato NOT YET / ALMOST / RIPE with a ripeness percentage, a colored bounding box, and a live count.
- Works with a live webcam, a photo, or a recorded video.
- Shows a **mask view** so you can see what the program segmented.
- Adjustable sliders for lighting and ripeness thresholds, plus an optional white balance.
- Logs readings with a true label to a CSV file, so you can measure accuracy.
- Saves snapshots of the annotated view.

## OpenCV techniques used

| Lab topic | What this project does |
|---|---|
| **a. Image Operations** | Mirror and resize frames, Gaussian blur, BGR to HSV conversion, gray-world white balance, drawing boxes and labels |
| **b. Image Segmentation** | HSV thresholding (`cv2.inRange`) into red, yellow-orange, and green masks; morphological opening and closing to clean them |
| **d. Image Analysis and Transformation** | Contour extraction, area filtering, bounding boxes, per-tomato color-share measurement, median hue and saturation |
| **e. Motion and Object Tracking** | Nearest-center matching to keep each tomato's ID between frames; label smoothing over recent frames |

Topics c (Haar cascades) and f (facial landmarks) are not used.

## How ripeness is decided

1. Each frame is blurred and converted to HSV.
2. Three masks are made: **red** (hue 0 up to the "Ripe up to hue" setting, plus hues 170-179 where red wraps around), **yellow-orange** (just above that), and **green** (hue 35-85). Pixels must also pass the saturation and brightness minimums.
3. Their union is cleaned with morphological opening and closing, and each large blob becomes one tomato.
4. Inside each tomato, the share of red, yellow-orange, and green pixels is measured.
5. `score = red share + 0.5 * yellow-orange share`
   - score >= 0.70 -> **RIPE**
   - score >= 0.35 -> **ALMOST**
   - otherwise -> **NOT YET**
6. The label shown is a majority vote over the tomato's most recent frames, so it does not flicker.

## Requirements

- Windows (the packaged `.exe` is built for Windows), or any system with Python
- Python with Tkinter (included in the standard Windows installer from python.org)
- A webcam, only if you want live mode
- Packages in `requirements.txt` (`opencv-python`, `numpy`)

Developed with Python 3.14 and OpenCV 5.0.0.

> Install `opencv-python`, **not** `opencv-python-headless`. The headless package has no windows and the app will not display.

## Setup

```
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

On macOS or Linux, activate with `source .venv/bin/activate`.

## How to run

**Desktop application (recommended):**

```
python tomato_app.py
```

**Packaged `.exe`:** download the zipped `TomatoRipeness` folder from `[ADD LINK: GitHub Release or shared drive]`, unzip it, and double-click `TomatoRipeness.exe` inside the unzipped folder. Do not run it from inside the zip. Windows may show an "unknown publisher" warning: click **More info**, then **Run anyway**.

**Simple OpenCV-window version:**

```
python tomato_ripeness.py              # live webcam
python tomato_ripeness.py photo.jpg    # one photo
python tomato_ripeness.py clip.mp4     # a recorded video
```

Keys (click the video window first): `q` or `Esc` quit, `w` white balance on/off, `s` save snapshot, `1` / `2` / `3` log visible tomatoes as NOT YET / ALMOST / RIPE, `h` show hue and saturation, `r` reset tracking.

## Using the application

- **Start Webcam / Open Image / Open Video / Stop** choose what is analyzed.
- **White balance** can reduce color casts from room lighting. It can also shift hues slightly, so keep it fixed while testing.
- **Show hue (H) and saturation (S)** prints each tomato's median hue and saturation on its label. Use it to tune the sliders.
- **Saturation min / Brightness min** decide which pixels count as colored. Lower them if a pale tomato is not filled in on the mask.
- **Ripe up to hue** decides how far into orange a tomato still counts as ripe.
- **Label smoothing** is the number of recent frames averaged for each label. Lower is faster but may flicker.
- **Log visible tomatoes with TRUE label** records the current readings together with the label you say is correct. Only press it when every visible tomato has that true ripeness.
- **Save Snapshot** saves the annotated view.

Logs, snapshots, and `error_log.txt` are saved next to the program (or next to the `.exe`).

**Tips for good results:** keep tomatoes apart (touching tomatoes count as one), use a plain light background such as white paper, use even light without glare, and keep hands out of view.

## Measuring accuracy

**On photos (batch):** put photos in folders named for the true ripeness. Every tomato in a photo must belong to that class. Photos with mixed ripeness go in `mixed` (annotated but not scored).

```
test_images/
    not_yet/
    almost/
    ripe/
    mixed/
```

```
python batch_image_test.py                       # uses the test_images folder
python batch_image_test.py my_photos 90 70 22    # folder, S min, V min, ripe hue
python evaluate_log.py image_test_log.csv        # confusion tables
```

Annotated copies of every photo are written to `image_test_output/`.

**Live:** use the Log buttons (or keys `1` / `2` / `3`) while testing, then run `python evaluate_log.py` to read `ripeness_log.csv`.

White balance ON and OFF are reported separately.

## Building the .exe

```
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --clean --windowed --onedir --name TomatoRipeness tomato_app.py
```

The result is `dist\TomatoRipeness\TomatoRipeness.exe`. The whole `dist\TomatoRipeness` folder must stay together. Use the same command without `--windowed` to see error messages in a console.

## Project structure

```
tomato_app.py          desktop application window (entry point for the .exe)
tomato_ripeness.py     detection, classification, tracking, and the simple OpenCV-window version
batch_image_test.py    scores a folder of photos
evaluate_log.py        builds confusion tables from a log file
requirements.txt       dependencies
sample_inputs/         sample photos and videos for testing
screenshots/           screenshots of the output
```

## Screenshots

`[ADD: screenshots of the application showing RIPE, ALMOST, and NOT YET tomatoes, and the mask view]`

## Limitations

- Color is only a proxy for ripeness. It says nothing about firmness or taste, and it cannot judge produce that stays green when ripe.
- Lighting changes the measured hue, and white balance can shift it further, so a tomato near a label boundary may change label.
- Touching tomatoes are merged into one blob and counted once.
- Skin and warm-colored backgrounds can look like tomato color.
- The thresholds were tuned on our own tomatoes and may not transfer to other varieties.

## Possible improvements

Separate touching tomatoes with watershed segmentation, calibrate lighting with a reference color card, add profiles for other fruit (strawberry, banana), and replace the fixed thresholds with a trained classifier.
