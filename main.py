from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from PIL import Image

from logic import plot_color_distribution, swap_stripes, image_to_base64

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Эндпоинт для главной страницы
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    # Возвращаем шаблон index.html и передаем в него контекст с запросом
    return templates.TemplateResponse("main_form.html", {"request": request})


# Эндпоинт для обработки изображения и отображения на странице
@app.post("/process_image/", response_class=HTMLResponse)
async def process_image(request: Request, file: UploadFile = File(...), stripe_width: int = Form(...), direction: str = Form(...)):
    # Открываем исходное изображение
    image = Image.open(file.file)

    # Обрабатываем изображение (меняем полосы местами)
    processed_image = swap_stripes(image, stripe_width, direction)

    # Конвертируем изображения в base64
    original_image_base64 = image_to_base64(image)
    processed_image_base64 = image_to_base64(processed_image)

    # Строим графики распределения цветов для исходного и измененного изображений
    original_color_distribution = plot_color_distribution(image)

    # Рендерим шаблон с изображениями и графиками
    return templates.TemplateResponse("display_images.html", {
        "request": request,
        "original_image": original_image_base64,
        "processed_image": processed_image_base64,
        "original_color_distribution": original_color_distribution,
    })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
