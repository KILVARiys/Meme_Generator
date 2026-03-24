// Предпросмотр изображения
const fileInput = document.getElementById('file_mem');

fileInput.onchange = function(evt) {
    const files = this.files;
    
    if (files && files.length > 0) {
        const file = files[0]; // Более надежный способ получения файла
        
        // Проверка типа файла
        if (!file.type.startsWith('image/')) {
            alert('Пожалуйста, выберите изображение');
            this.value = ''; // Очищаем поле выбора
            return;
        }
        
        // Проверка размера файла (16 MB)
        if (file.size > 16 * 1024 * 1024) {
            alert('Файл слишком большой. Максимальный размер 16 MB');
            this.value = '';
            return;
        }
        
        // Создаем или получаем элемент для предпросмотра
        let preview = document.getElementById('preview');
        if (!preview) {
            preview = document.createElement('img');
            preview.id = 'preview';
            preview.style.maxWidth = '100%';
            preview.style.marginTop = '20px';
            preview.style.borderRadius = '8px';
            preview.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
            this.parentNode.appendChild(preview);
        }
        
        // Отображаем предпросмотр
        preview.src = URL.createObjectURL(file);
        
        // Очищаем URL объекта после загрузки
        preview.onload = function() {
            URL.revokeObjectURL(this.src);
        };
    } else {
        // Если файл не выбран, удаляем предпросмотр
        const preview = document.getElementById('preview');
        if (preview) {
            preview.remove();
        }
    }
};