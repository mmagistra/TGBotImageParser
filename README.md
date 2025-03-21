# TGBotImageParser
Education project. Idea - create telegram bot which can parse web pages for images. You can also process the received images.

# Image formatting
- Formatting of the image is done using the Pillow library.

- All available methods can be found in the image_formatter.py file

- Any of methods return the path to the processed image.
- To use the methods, you need to create an object of the ImageFormatter class, add the path to the directory with default image which you want to process, then you can call the methods.