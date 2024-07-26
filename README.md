## This conversation saves your time about asnyc querysets
```
https://stackoverflow.com/questions/61926359/django-synchronousonlyoperation-you-cannot-call-this-from-an-async-context-u
```

## gunicorn
```
sudo nano /etc/systemd/system/gunicorn-secondapp.service
```

## Modify bot.py: Make your changes to the Python script.
## Restart the service: Restart the service to apply the changes to the script.
```
sudo systemctl restart uravo-bot.service
sudo systemctl restart gunicorn
sudo systemctl restart nginx

```