# Smile Score with Google App Engine (python3) and Flask

Smile Score is a web app to help you calculate the score of your smile. Just for fun!
It's using Google App Engine (python3) and Flask. 

GAE(py3) is much better than GAE(py2) in terms of the packages you can use. Now you can 
use client libraries directly by adding them into your requirements.txt file. 

## Installation

Activate your python3 environment, install the packages, run locally for test.

```bash
. ~/py3env/bin/activate
pip install -r requirements.txt
python main.py
```

## Deploy in GAE(python3)

   ```bash
   gcloud app deploy
   ```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

