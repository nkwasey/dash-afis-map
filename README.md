# dash-afis-map
This is a demo of the Dash interactive Python framework developed by Plotly and Dash displaying fire information for countries in West Africa.

# How to run this application
(The following instructions apply to Windows command line.)

To run this app first clone repository and then open a terminal to the app folder.

```
git clone https://github.com/nkwasey/dash-afis-map.git
cd afis-dash
```

# Create a virtual environment for your project
Create and activate a new virtual environment (recommended) by running the following:

On Windows (anaconda prompt)
In the terminal client enter the following where yourenvname is the name you want to call your environment, 
```
conda create --n yourenvname python=3.6
```

# Activate your virtual environment.
To activate or switch into your virtual environment, simply type the following where yourenvname is the name you gave to your environement at creation.
```
conda activate yourenvname 
```

Install the requirements:
```
pip install -r requirements.txt
```
Run the app:
```
python app1.py
```

You can run the app on your browser at http://127.0.0.1:8050

# Screenshot
![afis-dash screenshot2](https://user-images.githubusercontent.com/29225371/82278826-9c908c00-997a-11ea-9c9e-f7756b00ab12.PNG)

# Resources
### Data Sources:
- [EORIC-UENR](https://www.eoric.uenr.edu.gh/)
- [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/download/).
