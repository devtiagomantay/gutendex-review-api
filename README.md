# gutendex-review-api

This app allow the user search and review books from the gutendex api

Features:

1. An API consumer can search for books given a title. (Part 1)

2. An API consumer can post a review and a rating for a specific book. (Part 2)

3. An API consumer can get the details and the average rating of a specific book. (Part 3)

## How to run locally

- Change the permission of the script, type:
```
chmod 755 script.sh
```
- Run the script `script.sh`:
 ```
./script.sh
```

## Endpoints

The endpoints allow the user search a book, get a book details and review a book.

### Get book details by id
```
GET /books/details/id=<BOOK_ID>
```

### Search books by bookname
```
GET /books/search/name/<BOOK_NAME>
```

### Review a book
```
POST /books/review
PAYLOAD
{
    "bookId": 1,
    "rating": 5,
    "review": "This book is awesome!"
}
```

