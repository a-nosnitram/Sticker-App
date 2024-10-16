import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QColorDialog, QFileDialog
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtCore import Qt, QTranslator, QCoreApplication
from io import BytesIO


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Sticker_Maker(QtWidgets.QMainWindow):
    def __init__(self):
        super(Sticker_Maker, self).__init__()

        uic.loadUi(resource_path('resources/sticker_maker_ui.ui'), self)
        self.setWindowTitle("STICKER MAKER")

        # load translations
        self.translator = QTranslator(self)
        self.current_language = 'ru'  # Set default language to English
        self.load_language(self.current_language)

        # connect buttons
        self.file_upload_button.clicked.connect(self.upload_image)
        self.download_button.clicked.connect(self.save_image)
        self.colour_select_button.clicked.connect(self.select_colour)
        self.apply_caption_button.clicked.connect(self.apply_caption)
        self.clear_button.clicked.connect(self.clear)
        self.language_switch_button.clicked.connect(self.switch_language)

        self.image = None
        self.cleanImage = None
        self.captionColour = QColor(0, 0, 0)

    def load_language(self, lang_code):
        if lang_code == 'ru':
            self.translator.load(resource_path('translations_ru.qm'))
            self.language_switch_button.setText(
                "Switch to English")
        else:
            self.translator.load(resource_path('translations_en.qm'))
            self.language_switch_button.setText(
                "Переключить на русский")

        app.installTranslator(self.translator)

        # Update UI texts
        self.setWindowTitle(QCoreApplication.translate('Sticker_Maker', 'Стикер Мейкер'))
        self.file_upload_button.setText(QCoreApplication.translate('Sticker_Maker', 'Открыть Файл с Изображением'))
        self.download_button.setText(QCoreApplication.translate('Sticker_Maker', 'Скачать Стикер'))
        self.colour_select_button.setText(QCoreApplication.translate('Sticker_Maker', 'Выбрать Цвет'))
        self.apply_caption_button.setText(QCoreApplication.translate('Sticker_Maker', 'Применить'))
        self.clear_button.setText(QCoreApplication.translate('Sticker_Maker', 'Очистить'))
        self.language_switch_button.setText(QCoreApplication.translate('Sticker_Maker', 'Switch to English'))
        self.top_label.setText(QCoreApplication.translate('Sticker_Maker', 'Подпись Сверху'))
        self.bottom_label.setText(QCoreApplication.translate('Sticker_Maker', 'Подпись Снизу'))

    def switch_language(self):
        # Toggle language
        if self.current_language == 'en':
            self.current_language = 'ru'
        else:
            self.current_language = 'en'

        self.load_language(self.current_language)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def upload_image(self):

        selectedFile, _ = QFileDialog.getOpenFileName(self, QCoreApplication.translate(
            'Sticker_Maker', "Открыть Файл с Изображением"), "", "Image Files (*.png *.jpg *.bmp)")

        if selectedFile:

            self.image = Image.open(selectedFile).resize((512, 512))

            self.cleanImage = self.image.copy()

            ourImage = QPixmap(selectedFile).scaled(
                512, 512, aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.SmoothTransformation)

            self.display_image_label.setPixmap(ourImage)

    def select_colour(self):
        colour = QColorDialog.getColor()
        if colour.isValid():
            self.captionColour = colour

    def apply_caption(self):

        if self.image:
            topCaption = self.top_caption_lineEdit.text()
            bottomCaption = self.bottom_caption_lineEdit.text()

            captionFont = ImageFont.truetype("Impact.ttf", 60)

            drawing = ImageDraw.Draw(self.image)

            topBox = drawing.textbbox((0, 0), topCaption, font=captionFont)
            bottomBox = drawing.textbbox(
                (0, 0), bottomCaption, font=captionFont)

            topCaptionWidth = topBox[2] - topBox[0]
            bottomCaptionWidth = bottomBox[2] - bottomBox[0]

            topCaptionX = (512 - topCaptionWidth) / 2

            topCaptionY = 5

            bottomCaptionX = (512 - bottomCaptionWidth) / 2
            bottomCaptionY = 480 - (bottomBox[3] - bottomBox[1])

            drawing.text((topCaptionX, topCaptionY), topCaption,
                         font=captionFont, fill=self.captionColour.getRgb()[:3])
            drawing.text((bottomCaptionX, bottomCaptionY), bottomCaption,
                         font=captionFont, fill=self.captionColour.getRgb()[:3])

            imageBytes = BytesIO()
            self.image.save(imageBytes, format='PNG')
            imageBytes.seek(0)
            pixmap = QPixmap()
            pixmap.loadFromData(imageBytes.getvalue(), format='PNG')

            self.display_image_label.setPixmap(pixmap)

    def clear(self):
        if self.image:
            self.image = self.cleanImage.copy()

            imageBytes = BytesIO()
            self.image.save(imageBytes, format='PNG')
            imageBytes.seek(0)

            pixmap = QPixmap()
            pixmap.loadFromData(imageBytes.getvalue(), format='PNG')

            self.display_image_label.setPixmap(pixmap)

    def save_image(self):
        if self.image:
            if len(self.top_caption_lineEdit.text()) > 0 and len(self.bottom_caption_lineEdit.text()) == 0:
                name = self.top_caption_lineEdit.text()
            elif len(self.bottom_caption_lineEdit.text()) > 0 and len(self.top_caption_lineEdit.text()) == 0:
                name = bottom_caption_lineEdit.text()
            elif len(self.top_caption_lineEdit.text()) > 0 and len(self.bottom_caption_lineEdit.text()) > 0:
                name = self.top_caption_lineEdit.text() + " " + self.bottom_caption_lineEdit.text()
            else:
                name = QCoreApplication.translate("Sticker_Maker", "Стикер")

            save_path = QFileDialog.getSaveFileName(self, QCoreApplication.translate(
                "Sticker_Maker", "Скачать Стикер"), f"{name}.png", "PNG Files (*png)")
            if save_path[0]:
                self.image.save(save_path[0], "PNG")

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


app = QtWidgets.QApplication(sys.argv)
window = Sticker_Maker()
window.show()
sys.exit(app.exec_())
