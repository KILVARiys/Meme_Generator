import uuid
import os

from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        text_up = request.form.get('text_up', '')
        text_low = request.form.get('text_low', '')
        
        if file and file.filename:
            # Сохраняем загруженный файл
            filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Открываем изображение
            image = Image.open(filepath)

            # Конвертируем в RGB для совместимости с JPEG
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Создаем объект для рисования и шрифт
            drawer = ImageDraw.Draw(image)
            font = ImageFont.truetype("arial.ttf", 25)
            
            # Позиция для верхнего текста (центрируем по горизонтали)
            if text_up:
                # Получаем размер верхнего текста
                bbox = drawer.textbbox((0, 0), text_up, font=font)
                text_width = bbox[2] - bbox[0]
                x_up = (image.width - text_width) // 2
                y_up = 50  # отступ сверху
                drawer.text((x_up, y_up), text_up, font=font, fill='black')
            
            # Позиция для нижнего текста (центрируем по горизонтали, прижимаем к низу)
            if text_low:
                # Получаем размер нижнего текста
                bbox = drawer.textbbox((0, 0), text_low, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x_low = (image.width - text_width) // 2
                y_low = image.height - text_height - 50  # отступ снизу
                drawer.text((x_low, y_low), text_low, font=font, fill='black')
            
            # Сохраняем результат
            output_filename = f"meme_{uuid.uuid4()}.jpg"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            image.save(output_path)

            # После сохранения результата, удаляем оригинал
            os.remove(filepath)

            return render_template('result.html', filename=output_filename)
    
    return "Ошибка при загрузке", 400  # если что-то пошло не так

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/download/<filename>', methods=['GET'])
def download_file():
    pass

if __name__ == '__main__':
    app.run(debug=True)