import discord
from discord.ext import commands
from imageai.Detection import ObjectDetection
from PIL import Image
import os

# Инициализация бота
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Путь к модели и детектору
model_path = "./yolov3.pt"  # Убедись, что путь правильный
detector = ObjectDetection()

# Инициализация модели
detector.setModelTypeAsYOLOv3()
detector.setModelPath(model_path)
detector.loadModel()

# Функция для обработки изображения
async def detect_objects(image_path):
    # Детекция объектов с использованием ImageAI
    image = Image.open(image_path)
    detections = detector.detectObjectsFromImage(input_image=image_path, output_image_path="output_image.jpg")
    
    # Получение результатов
    result = []
    for eachObject in detections:
        result.append(f"{eachObject['name']} {eachObject['percentage_probability']}%")
    
    return result

# Обработчик команд бота
@bot.event
async def on_ready():
    print(f'Bot Connected: {bot.user}')

@bot.event
async def on_message(message):
    if message.content.startswith('!detect') and message.attachments:
        # Загружаем изображение
        attachment = message.attachments[0]
        file_name = "temp_image.jpg"
        await attachment.save(file_name)

        # Обработка изображения
        detection_results = await detect_objects(file_name)
        
        # Отправка результатов
        await message.channel.send("\n".join(detection_results))

        # Удаление временного файла
        os.remove(file_name)

bot.run("MTI4NDc3OTAzODg4NzM4MzE0Mw.Gx6a-T.bT8JhiMrWYm65092eOUwXbWNtObnoNfP9euWIM")  # Вставь свой токен