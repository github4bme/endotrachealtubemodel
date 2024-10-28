# Machine Learning Integrated to Endotracheal Tube Insertion

### Programs In This Project

1. #### train.py
    Trains a model based on a current version of a model and new data to add to its training data.

2. #### test.py
    Validates the model, and outputs the result to a new directory within runs/detect/ called valN, where N is the next available number of run.

3. #### predict.py
    Runs the model through a video, predicting the locations of features in the video. There is the option to playback the video as it predicts, or save the predicted video to a new file in full_predicted_videos/.

4. #### convert_format_and_train_test_split.py
    Converts the data format from the downloaded CVAT annotations to the format we need.

### Model Notes
As of 9-16-24, the value of 
```
model.names
```
from the most recent model (runs/detect/train3/weights/best.pt) is:
```
{0: 'trachea', 1: 'epiglottis', 2: 'uvula'}
```
Model Training/Data History:
| Date | New Trained Model Version | Additional Video(s) Trained On | Notes |
| - | - | - | - |
| Start of Autumn 2024 semester | runs/detect/train3/weights/best.pt | N/A |
| 10-25-2024 | runs/detect/train5/weights/best.pt | 047217044_001 | I ended this training after 20 epochs |

Model Testing History:
| Date | Test Results Directory | Model File Tested | Dataset Tested On |
| - | - | - | - |
| 10-28-2024 | runs/detect/val11 | runs/detect/train3/weights/best.pt | 047217044_001 |
| 10-28-2024 | runs/detect/val12 | runs/detect/train5/weights/best.pt | 047217044_001 |

### Instructions for preparing data for training using CVAT

1. Create an account and organization on CVAT:

    ![CVAT org creation](images/cvat_org_creation.png)

    When working on this project in CVAT, make sure you are in the correct organization, not "Personal Workspace" or another organization.

2. Create a new project within this organization. When creating the project, be sure to add the labels: ['trachea', 'epiglottis', 'uvula']. It's important to ensure the order is consistent with the class label numbers (trachea = 0, etc.).

    ![CVAT project creation 1](images/cvat_project_creation_1.png)
    ![CVAT project creation 2](images/cvat_project_creation_2.png)

3. Download the video you want to annotate from the google sheet titled
["Video Annotation Progress"](https://docs.google.com/spreadsheets/d/1T86gqUQacowGvsDeFqO6eBcgxWp41lqLjR3G9PPORe8/edit?usp=sharing).

4. Navigate to this project and create a new task for each video you want to annotate. Upload the desired video to this task.

    ![CVAT task creation 1](images/cvat_task_creation_1.png)
    ![CVAT task creation 1](images/cvat_task_creation_2.png)

5. Within the task, click the job.

    ![CVAT job](images/cvat_job.png)

6. Annotation instructions:
    1. Navigate through the frames of the video using the buttons above the video or using the left and right arrow keys. When you see a feature, click the rectangle on the left. Click the correct feature name, Drawing Method: By 2 Points, and then Track.

    ![CVAT annotation 1](images/cvat_annotation_1.png)

    2. As you advance through the video, move the annotation box appropriately. Make sure to press the save button often. You can use the "v" key to skip forward 10 frames. If you then move the feature annotation box on this frame, CVAT will interpolate the annotation for the middle 9 frames. Note that this may not be the most accurate, but is usually helpful.

    3. If a feature is no longer visible, press the button on the right to "Switch outside property". You will then have to redraw the box if/when the feature reappears.

    ![CVAT annotation 2](images/cvat_annotation_2.png)

7. When you are finished annotating, return back to the job. Click export annotations.

    ![Export annotation 1](images/export_annotation_1.png)

8. Select "YOLOv8 Detection 1.0" for Export Format and name the dataset the same as the video name. Download the zip.

    ![Export annotation 2](images/export_annotation_2.png)

9. Extract the contents of the zip and place it in this repo in the folder: datasets_exported_from_cvat/ along with the source video file. There is a paywall to export the images along with the labels from CVAT so we need to extract them from the video.

    ![Export annotation 3](images/export_annotation_3.png)

10. Run convert_format_and_train_test_split.py with the correct dataset name. After running this, the dataset should be ready to further train a previous model version.

    ![Convert format](images/convert_format.png)