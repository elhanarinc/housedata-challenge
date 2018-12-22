# Plentific Challenge
Pletific coding challenge written with Django Framework.

This project assumes you had already installed these tools:
1. [python 3](https://realpython.com/installing-python/)
2. [pip](https://www.makeuseof.com/tag/install-pip-for-python/)
3. [postgresql](http://postgresguide.com/setup/install.html)

After necessary tools, you need to install the `sold house pricing` dataset from [here](https://data.gov.uk/dataset/4c9b7641-cf73-4fd9-869a-4bfeed6d440e/hm-land-registry-price-paid-data).

Then you need to add header row for this raw data by using command below on terminal:
* `echo 'transaction_unique_identifier,price,date_of_transfer,postcode,property_type,old_or_new,duration,paon,saon,street,locality,town,district,country,ppd_category_type,record_status' | cat - latest.csv > temp && mv temp latest.csv`

In order to use django with postgresql, you need to follow this [link](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04).

Below are the commands that is need for populating the empty postgresql table, then running the API:
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py populate_db [file-location]`
* `python manage.py runserver`
