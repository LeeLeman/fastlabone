import base64

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import io


# Функция для обмена полос изображения
def swap_stripes(image: Image, stripe_width: int, direction: str) -> Image:
    np_image = np.array(image)
    height, width, _ = np_image.shape
    stripes = []
    new_image = np.zeros_like(np_image)

    if direction == "vertical":
        for i in range(0, width, stripe_width):
            stripe = np_image[:, i:i + stripe_width]
            stripes.append(stripe)

        for i in range(0, len(stripes) - 1, 2):
            stripes[i], stripes[i + 1] = stripes[i + 1], stripes[i]

        new_image = np.concatenate(stripes, axis=1)

    # Делим изображение на полосы по горизонтали
    elif direction == "horizontal":
        for i in range(0, height, stripe_width):
            stripe = np_image[i:i + stripe_width, :]
            stripes.append(stripe)

        for i in range(0, len(stripes) - 1, 2):
            stripes[i], stripes[i + 1] = stripes[i + 1], stripes[i]

        new_image = np.concatenate(stripes, axis=0)

    return Image.fromarray(new_image)


# Функция для построения графика распределения цветов
def plot_color_distribution(image: Image) -> str:
    np_image = np.array(image)

    r, g, b = np_image[:, :, 0], np_image[:, :, 1], np_image[:, :, 2]

    # Создаем гистограммы для каждого канала с логарифмической шкалой по оси Y
    plt.figure(figsize=(10, 6))
    plt.hist(r.ravel(), bins=256, color='red', alpha=0.5, label='Красный канал')
    plt.hist(g.ravel(), bins=256, color='green', alpha=0.5, label='Зелёный канал')
    plt.hist(b.ravel(), bins=256, color='blue', alpha=0.5, label='Синий канал')

    # Настраиваем график
    plt.xlabel('Интенсивность цвета')
    plt.ylabel('Частота (логарифмическая)')
    plt.legend(loc='upper right')
    plt.title('Распределение цветов по каналам (RGB)')
    plt.yscale('log')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_str


def image_to_base64(image: Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_str
