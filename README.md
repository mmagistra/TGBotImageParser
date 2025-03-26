# TGBotImageParser
Education project. Idea - create telegram bot which can parse web pages for images. You can also process the received images.

# Image formatting
- Formatting of the image is done using the Pillow library.
- All available methods can be found in the image_formatter.py file
- Example of image process you can find in: images/example_parsed_images/source_link/image_name
- Any of methods return the path to the processed image.
- To use the methods, you need to create an object of the ImageFormatter class, add the path to the directory with default image which you want to process, then you can call the methods.
- Methods can raise exceptions if the directory is not selected or if selected mode is not available. In this case, you can use the select_image_directory method to select the directory with the default image.
- Also, methods can raise exceptions if the image format is not suitable for the selected method.

# Photo parsing and downloading
- Parsing is performed by libraries: BeautifulSoup, requests, aiohttp.
- A single function scrape_and_save_images(address) is available, where address is a link to the site in str format.
- The function returns 'done' in case of successful completion of the program or returns the text in string format with an error.
- Images are saved in the path images/parsed_images/* , where * is [image_name]/default.png (possible extensions are png, jpeg, jpg). 
