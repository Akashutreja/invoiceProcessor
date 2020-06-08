# invoice-processor
## please follow these steps to run project
1. After cloning this reposiroty. cd invoiceProcessor 
2. pip install -r requirements.txt
3. create database in postgres terminal with name "invoice".
4. Run python manage.py migrate in "invoice-processor" directory
5. create superuser python manage.py createsuperuser then enter credentials
6. go to http://127.0.0.1:8000/admin/ then enter credentials here you can create raw data of invoice 
or
Use data dump that is provided you over the email and use this command "psql invoice < path to invoice.sql" where invoice is database name.
