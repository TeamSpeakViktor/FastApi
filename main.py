from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)

@app.get("/", summary='Главная ручка', tags=['Основные ручки'])
def root():
    return 'Hello World'

books = [
    {
        "id": 1,
        "title": "Теория тестирования",
        "author": "Роман Савин",
    },

    {   
        "id": 2,
        "title": "Программирование Python",
        "author": "Валерий Михалков",
    },
]

@app.get("/books",
        tags=['Книги'],
        summary="Получить все книги", )

def read_books():
    return books


@app.get("/books/{book_id}",
         tags=['Книги'],
         summary="Получить книгу по ID",
         )

def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
        raise HTTPException(status_code=404, detail="Книга не найдена")
class NewBook(BaseModel):
    title: str
    author: str

@app.post("/books",
         tags=['Книги'],
         summary="Добавить книгу",
         )
def create_book(new_book:NewBook):
    books.append ({
        "id": len(books)+1,
        "title":new_book.title,
        "author":new_book.author,
    })
    return {"succes":True, "message": "Книга успешно добавлена"}

@app.delete("/books/{book_id}",
         tags=['Книги'],
         summary="Удалить книгу",
         )
async def delete_item(book_id: int):
    if book_id < 0 or book_id >= len(books):
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted_item = books.pop(book_id)
    return deleted_item