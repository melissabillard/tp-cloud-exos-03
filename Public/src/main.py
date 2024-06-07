from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modèle Pydantic pour représenter un Animal
class Animal(BaseModel):
    id: int
    name: str
    species: str

# Base de données en mémoire (liste) pour stocker les animaux
animals_db = [
    {"id": 1, "name": "Fluffy", "species": "Cat"},
    {"id": 2, "name": "Rex", "species": "Dog"},
    {"id": 3, "name": "Goldie", "species": "Fish"}
]

# Routes pour gérer les animaux

@app.get("/animals", response_model=List[Animal])
async def get_animals():
    return animals_db

@app.post("/animals", response_model=Animal, status_code=201)
async def create_animal(animal: Animal):
    if any(a['id'] == animal.id for a in animals_db):
        raise HTTPException(status_code=400, detail="Animal with this ID already exists")
    animals_db.append(animal.dict())
    return animal

@app.get("/animals/{animal_id}", response_model=Animal)
async def get_animal(animal_id: int):
    animal = next((a for a in animals_db if a["id"] == animal_id), None)
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal

@app.put("/animals/{animal_id}", response_model=Animal)
async def update_animal(animal_id: int, updated_animal: Animal):
    for i, animal in enumerate(animals_db):
        if animal["id"] == animal_id:
            animals_db[i] = updated_animal.dict()
            return updated_animal
    raise HTTPException(status_code=404, detail="Animal not found")

@app.delete("/animals/{animal_id}", response_model=Animal)
async def delete_animal(animal_id: int):
    animal = next((a for a in animals_db if a["id"] == animal_id), None)
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    animals_db.remove(animal)
    return animal

# Route de base
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
