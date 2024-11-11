from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Initialize FastAPI
app = FastAPI()

# Serve static files (for CSS/JS if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mock Database
items = []

# Pydantic model for Item
class Item(BaseModel):
    name: str
    description: str

# Routes

# Serve HTML Page
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

# API to get items
@app.get("/api/items", response_model=List[Item])
async def get_items():
    return items

# API to create a new item
@app.post("/api/items")
async def create_item(name: str = Form(...), description: str = Form(...)):
    item = Item(name=name, description=description)
    items.append(item)
    return item

# HTML Template (placed in a string for simplicity here, but should be in `templates/index.html` in a real app)
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastAPI Full-Stack App</title>
    <script>
        async function fetchItems() {
            const response = await fetch("/api/items");
            const items = await response.json();
            document.getElementById("items").innerHTML = items.map(item => 
                `<li>${item.name}: ${item.description}</li>`
            ).join("");
        }

        async function addItem(event) {
            event.preventDefault();
            const formData = new FormData(document.getElementById("itemForm"));
            const response = await fetch("/api/items", {
                method: "POST",
                body: formData
            });
            const item = await response.json();
            document.getElementById("items").innerHTML += `<li>${item.name}: ${item.description}</li>`;
            document.getElementById("itemForm").reset();
        }

        document.addEventListener("DOMContentLoaded", fetchItems);
    </script>
</head>
<body>
    <h1>FastAPI Full-Stack App</h1>
    <form id="itemForm" onsubmit="addItem(event)">
        <input type="text" name="name" placeholder="Item Name" required>
        <input type="text" name="description" placeholder="Item Description" required>
        <button type="submit">Add Item</button>
    </form>
    <ul id="items"></ul>
</body>
</html>
"""

# Serve the HTML content directly (for single-file simplicity)
@app.get("/templates/index.html", response_class=HTMLResponse)
async def get_index():
    return HTMLResponse(content=html_content, status_code=200)
