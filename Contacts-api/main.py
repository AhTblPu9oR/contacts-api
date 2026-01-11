from fastapi import FastAPI
from routers import contacts
from routers import products

app = FastAPI(
    title="Contacts API",
    description="A simple address book API",
    version="1.0.0"
)

app.include_router(contacts.router)
app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "Welcome to Contacts API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8800)