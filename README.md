# Visual Acad AI

## Local Setup
Create and activate a virtual environment with python 3.11, preferably using conda. One can install conda by following the steps [here](https://developers.google.com/earth-engine/guides/python_install-conda)
```
conda create -n vacad python=3.11
conda activate vacad
```

Install python requirements
```
pip install -r requirements.txt
```

Launch the application using the launch script
```
uvicorn app:app --host 0.0.0.0  
```