# bank

use this examples on your .env file
```
POSTGRES_HOST=book_db
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432

```

### Up all container using docker compose
```
make up-all
```

### Create database
```
make create-db
```

### Check api logs
```
make logs-api
```

### Run unit tests
```
make test
```

### Access api documentation on your browser
[swagger](http://127.0.0.1:8000/docs/)

[ReDoc](http://127.0.0.1:8000/redoc/)

### Search for books
```
curl --request GET \
  --url 'http://localhost:8000/v1/books?title=republic'
```

### Searching for books
```
curl --request POST \
  --url http://localhost:8000/v1/books/review \
  --header 'Content-Type: application/json' \
  --data '{
	"bookId":11,
	"rating": 4,
	"review": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'\''s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
}'
```

### Reviewing a book
```
curl --request GET \
  --url http://localhost:8000/v1/books/1
```
