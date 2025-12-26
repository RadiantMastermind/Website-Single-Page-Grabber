# Grapper for a Single web page
# (c) Copyright by Radiant Mastermind
# if you want to use this code for your project - just include my name or donate via dotation-arlets in py Git profile
# https://github.com/RadiantMastermind

import requests
from bs4 import BeautifulSoup
import re
import shutil
import os
import json

allowed_types = [
    # Изображения
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/gif",
    "image/bmp",
    "image/webp",
    "image/svg+xml",
    "image/tiff",
    "image/x-icon",
    "image/vnd.microsoft.icon",
    "image/heif",
    "image/heic",
    "image/avif",
    "image/apng",
    # Видео
    "video/mp4",
    "video/mpeg",
    "video/avi",
    "video/quicktime",
    "video/x-ms-wmv",
    "video/x-flv",
    "video/webm",
    "video/x-matroska",
    "video/ogg",
    "video/3gpp",
    "video/3gpp2",
    # Аудио
    "audio/mpeg",
    "audio/wav",
    "audio/wave",
    "audio/ogg",
    "audio/mp4",
    "audio/aac",
    "audio/flac",
    "audio/x-ms-wma",
    "audio/opus",
    # Документы и текстовые файлы
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "text/plain",  # TXT файлы
    "text/richtext",
    "text/csv",
    "text/html",
    "text/css",
    "text/javascript",  # JS файлы
    "application/javascript",
    "application/x-javascript",
    # Данные
    "application/json",
    "application/xml",
    "text/xml",
    # OpenDocument
    "application/vnd.oasis.opendocument.text",
    "application/vnd.oasis.opendocument.spreadsheet",
    "application/vnd.oasis.opendocument.presentation",
    # Архивы
    "application/zip",
    "application/x-rar-compressed",
    "application/x-7z-compressed",
    "application/x-tar",
    "application/gzip",
    "application/x-bzip2",
    # Исходный код
    "text/x-python",
    "text/x-java-source",
    "text/x-c",
    "text/x-c++",
    "text/x-php",
    # Графика и дизайн
    "application/x-shockwave-flash",
    "image/vnd.adobe.photoshop",
    "application/postscript",
    "application/illustrator",
    # Шрифты
    "font/ttf",
    "font/otf",
    "font/woff",
    "font/woff2",
]

print("MIME ADDED. PROGRAM STARTED")

# Inputing page

page = input("Enter your target page here: ")
req = requests.get(page)
print(f"REQUEST STATUS CODE: {req.status_code}")

targetpage = BeautifulSoup(req.content, "html.parser")
print(targetpage.prettify())

print(f"Your target page is: {page}")



# Starting program

bodytag = targetpage.find("body")  # Tag of website

while True:
    grab = input("Grab data from this page? [Y/N]: ")
    if grab.upper() == "Y":

        inputdata = input(
            "ENTER TAG TO EXTRACT DATA (format: tag class attribute OR tag attribute): "
        )
        inputdata_parts = inputdata.split()

        if len(inputdata_parts) == 3:
            # Формат: тег класс атрибут
            tag_name = inputdata_parts[0]
            class_name = inputdata_parts[1]
            attribute_name = inputdata_parts[2]

            if bodytag:
                elements = bodytag.find_all(tag_name, class_=class_name)
                if elements:
                    for findobject in elements:
                        if attribute_name.lower() == "text":
                            print(f"Found text: {findobject.text.strip()}")
                        elif attribute_name in findobject.attrs:
                            print(
                                f"Found attribute '{attribute_name}': {findobject[attribute_name]}"
                            )
                        else:
                            print(f"Attribute '{attribute_name}' not found")
                else:
                    print("Not found")

        elif len(inputdata_parts) == 2:
            # Проверяем, является ли второй параметр классом или атрибутом
            tag_name = inputdata_parts[0]
            second_param = inputdata_parts[1]

            if bodytag:
                # Сначала пробуем найти по классу
                elements_by_class = bodytag.find_all(tag_name, class_=second_param)

                if elements_by_class:
                    for findobject in elements_by_class:
                        print(f"Found text: {findobject.text.strip()}")
                else:
                    # Если не нашли по классу, ищем все теги и проверяем атрибут
                    elements = bodytag.find_all(tag_name)
                    if elements:
                        for findobject in elements:
                            if second_param.lower() == "text":
                                print(f"Found text: {findobject.text.strip()}")
                            elif second_param in findobject.attrs:
                                print(
                                    f"Found attribute '{second_param}': {findobject[second_param]}"
                                )
                            else:
                                # Проверяем все атрибуты, содержащие этот параметр
                                for attr_name, attr_value in findobject.attrs.items():
                                    if second_param in attr_name:
                                        print(
                                            f"Found attribute '{attr_name}': {attr_value}"
                                        )
                    else:
                        print("Not found")

        elif len(inputdata_parts) == 1:
            # Просто тег - выводим текст
            if bodytag:
                elements = bodytag.find_all(inputdata_parts[0])
                if elements:
                    for findobject in elements:
                        print(f"Found text: {findobject.text.strip()}")
                else:
                    print("Not found")
        else:
            print("Please enter 1, 2 or 3 words separated by space")

    else:
        break

end = input("Press any key to exit")
