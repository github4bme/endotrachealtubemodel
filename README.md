# Machine Learning Integrated to Endotracheal Tube Insertion

### Programs In This Project
<ol>

<li>
<h4>train.py</h4>
<div>
TODO
</div>
</li>

<li>
<h4>test.py</h4>
<div>
Validates the model, and outputs the result to a new directory within
runs/detect/ called valN, where N is the next available number of run.
</div>
</li>

<li>
<h4>predict.py</h4>
<div>
Runs the model through a video, predicting the locations of features in the video.
</div>
</li>

</ol>


### Model Notes
As of 9-16-24, the value of 
```
model.names
```
from the most recent model (runs/detect/train3/weights/best.pt) is:
```
{0: 'trachea', 1: 'epiglottis', 2: 'uvula'}
```

### Instructions for preparing data for training
TODO