import csv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Path to the CSV file
CSV_FILE_PATH = "Details.csv"

# In-memory database (for demonstration purposes)
items = []

# Pydantic model for item data
class Item(BaseModel):
    name: str
    course: str
    year: int


# Save items to CSV file
def save_items_to_csv():
    with open(CSV_FILE_PATH, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "course", "year"])
        writer.writeheader()
        for item in items:
            writer.writerow({"name": item.name, "course": item.course, "year": item.year})

# Create an item and save to CSV
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    save_items_to_csv()  # Save to CSV after creating an item
    return item

# Read an item by its ID
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
