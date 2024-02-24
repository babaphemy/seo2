from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(
    tags=['home']
)
@router.get("/")
def home():
    base_path = "ReachAI"
    body = f"""
    <head>
    <style>
    .product {{ 
        width: 500px;
        height: 30px;
        border: 2px inset green;
        padding: 2px;
        border-radius: 8px;
        background-color: lightblue;
        text-align: center;
         position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
    }}
    </style>
    </head>
    <div class="product">{base_path}</div>
    """
    return HTMLResponse(content=body, media_type="text/html")