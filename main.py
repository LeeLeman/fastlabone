import httpx
import uvicorn
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image

import settings
from logic import image_to_base64, plot_color_distribution, swap_stripes

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Эндпоинт для главной страницы с формой
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(
        "main_form.html", {"request": request, "site_key": settings.SITE_KEY}
    )


# Эндпоинт для обработки изображения и отображения на странице
@app.post("/process_image/", response_class=HTMLResponse)
async def process_image(
    request: Request,
    file: UploadFile = File(...),
    stripe_width: int = Form(...),
    direction: str = Form(...),
    g_recaptcha_response: str = Form(alias="g-recaptcha-response"),
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": settings.SECRET_KEY, "response": g_recaptcha_response},
        )
    result = response.json()

    captcha_check = g_recaptcha_response and result.get("success")
    if not captcha_check:
        return templates.TemplateResponse(
            "main_form.html",
            {
                "request": request,
                "site_key": settings.SITE_KEY,
                "error": "Проверка капчи не пройдена. Пожалуйста, попробуйте ещё раз",
            },
        )

    if not file.size:
        return templates.TemplateResponse(
            "main_form.html",
            {
                "request": request,
                "site_key": settings.SITE_KEY,
                "error": "Не выбрано изображение. Пожалуйста, попробуйте еще раз",
            },
        )

    image = Image.open(file.file)

    processed_image = swap_stripes(image, stripe_width, direction)
    original_image_base64 = image_to_base64(image)
    processed_image_base64 = image_to_base64(processed_image)
    original_color_distribution = plot_color_distribution(image)

    return templates.TemplateResponse(
        "display_images.html",
        {
            "request": request,
            "message": "Капча пройдена! Изображение обработано.",
            "original_image": original_image_base64,
            "processed_image": processed_image_base64,
            "original_color_distribution": original_color_distribution,
        },
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
