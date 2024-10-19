from io import BytesIO

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_form_load():
    """
    Тест на загрузку главной страницы с формой.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "Загрузите изображение для обработки" in response.text


def test_no_file_selected(mocker):
    """
    Тест на случай, если файл не был выбран.
    """
    mocker.patch("httpx.AsyncClient.post", return_value=mocker.Mock(status_code=200, json=lambda: {"success": True}))

    file_data = BytesIO(b"")

    response = client.post("/process_image/",
       files={"file": ("filename.png", file_data, "image/png")},
       data={
           "stripe_width": "10",
           "direction": "horizontal",
           "g-recaptcha-response": "VALID_CAPTCHA_RESPONSE"
           }
       )
    assert response.status_code == 200
    assert "Не выбрано изображение. Пожалуйста, попробуйте еще раз" in response.text


def test_invalid_recaptcha(mocker):
    """
    Тест на неудачную проверку капчи.
    """
    mocker.patch("httpx.AsyncClient.post", return_value=mocker.Mock(status_code=200, json=lambda: {"success": False}))

    file_data = BytesIO(b"dummy data")

    response = client.post("/process_image/",
        files={"file": ("filename.png", file_data, "image/png")},
        data={
            "stripe_width": "10",
            "direction": "horizontal",
            "g-recaptcha-response": "INVALID_CAPTCHA_RESPONSE"
        }
    )

    assert response.status_code == 200
    assert "Проверка капчи не пройдена. Пожалуйста, попробуйте ещё раз" in response.text
