# COVID-detector-Web

This project developed by Flask

Google cloud deploy:
<br/>$gcloud config set project <PROJECT_ID>
<br/>$gcloud app deploy
<br/>$gcloud app browse

 <br/> git config --global user.email "you@example.com"
 <br/> git config --global user.name "Your Name"

Run Flask:
<br/> >$env:FLASK_APP="test.py" 
<br/> >flask run
or
<br/> >set FLASK_APP=test.py

Anaconda configuration:
<br/> >conda info --envs
<br/> >conda activate COVID-detector-Web-master 


Debug Error:
"ImportError('Could not import PIL.Image. ' working with keras-ternsorflow"
<br/> conda uninstall --force pillow
<br/> pip install pillow
