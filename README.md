# Plentific

Author: Jan Chmelicek

Implements two APIs: for average property sale prices and API for 
histogram with 8 bins.

Plenty of stuff could be optimised way further. Just a few things that come to 
my mind:

  - histogram API's query could be transformed into materialised view, so that the
  query is rather quick
  - uploading CSV into DB should be done "offline", i.e. using COPY command and 
  perhaps temp table would be way easier.
  - I haven't touched anything related to authentication and such.
  - Whole developer experience might be enhanced - I've just used requirements.txt
  and fed it into pip3. I guess poetry could be a good replacement.
  - Browsable API should be fully configured + Swagger would help too.

## Running locally

```bash
docker-compose up
```

### Available APIs:

#### Average prices:

- GET 
- http://127.0.0.1:8000/price/averages/from_date/YYYY-MM-DD/to_date/YYYY-MM-DD/postcode/<postcode>/

#### Histogram:

GET http://127.0.0.1:8000/price/counts/from_date/YYYY-MM-DD/to_date/YYYY-MM-DD/postcode/<postcode>/


### Seeding data

```bash
docker-compose run plentific bash
python3 manage.py load_property_sales
```


### Adding a user

```bash
docker-compose run plentific bash
python3 manage.py createsuperuser
```

## Testing

```bash
docker-compose run plentific test
```
