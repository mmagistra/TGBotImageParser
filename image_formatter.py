from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw
import os


class ImageDirectoryNotSelected(Exception):
    pass


class UnknownMode(Exception):
    pass



class ImageFormatter:
    def __init__(self, default_path='images/parsed_images'):
        self.default_path = default_path
        self.current_image_directory = None
        self.current_image_format = None

        if not os.path.exists(self.default_path):
            os.makedirs(self.default_path)

    def select_image_directory(self, directory_path):
        """
        Select the directory with the image to be processed.

        Args:
            directory_path (str): The path to the directory with the image.

        Raises:
            ImageDirectoryNotSelected: If the directory is not selected or if the default image is not found in the directory.

        Notes:
            The image which will be processed is the one with the name "default.{image_format}" in the selected directory.
        """
        if directory_path[-1] != '/':
            directory_path += '/'
        self.current_image_directory = directory_path
        for f in os.listdir(directory_path):
            if f.split('.')[0] == 'default':
                self.current_image_format = f.split('.')[-1]

        if self.current_image_format is None:
            raise ImageDirectoryNotSelected(f'Cannot find default image in directory {directory_path}')

    def rotate_image(self, angle):
        """
        Rotate the current image by a specified angle.

        Args:
            angle (int or float): The angle in degrees to rotate the image. Positive values rotate counterclockwise,
                                  and negative values rotate clockwise.

        Returns:
            str: The path to the rotated image.

        Raises:
            ImageDirectoryNotSelected: If the current image directory is not selected.
        """
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            image = image.rotate(angle)
            image.save(self.current_image_directory + 'rotated.' + self.current_image_format)
        return self.current_image_directory + 'rotated.' + self.current_image_format

    def flip_image(self, mode='horizontal'):
        """
        Flip the current image either horizontally or vertically.

        Args:
            mode (str, optional): The mode to flip the image.
                                  Options are 'horizontal' or 'vertical'.
                                  Defaults to 'horizontal'.

        Returns:
            str: The path to the flipped image.

        Raises:
            ImageDirectoryNotSelected: If the current image directory is not selected.
            UnknownMode: If the flip mode is not recognized.
        """
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        if mode == 'horizontal':
            axis = Image.FLIP_LEFT_RIGHT
        elif mode == 'vertical':
            axis = Image.FLIP_TOP_BOTTOM
        else:
            raise UnknownMode('Unknown flip mode')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            image = image.transpose(axis)
            image.save(self.current_image_directory + 'flipped_' + mode + '.' + self.current_image_format)
        return self.current_image_directory + 'flipped_' + mode + '.' + self.current_image_format

    def crop_image(self, x_percent, y_percent, width_percent, height_percent):
        """
        Crop the current image based on specified percentages.

        Args:
            x_percent (float): The percentage from the left to start the crop.
            y_percent (float): The percentage from the top to start the crop.
            width_percent (float): The percentage of the original width to include in the crop.
            height_percent (float): The percentage of the original height to include in the crop.

        Returns:
            str: The path to the cropped image.

        Raises:
            ImageDirectoryNotSelected: If the current image directory is not selected.
        """
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            width, height = image.size
            x = int(width * x_percent / 100)
            y = int(height * y_percent / 100)
            crop_width = int(width * width_percent / 100)
            crop_height = int(height * height_percent / 100)
            cropped_image = image.crop((x, y, x + crop_width, y + crop_height))
            cropped_image.save(self.current_image_directory + 'cropped.' + self.current_image_format)
        return self.current_image_directory + 'cropped.' + self.current_image_format

    def resize_image(self, width_percent, height_percent):
        """
        Resize the current image based on specified percentages.

        Args:
            width_percent (float): The percentage of the original width to set as the new width.
            height_percent (float): The percentage of the original height to set as the new height.

        Returns:
            str: The path to the resized image.

        Raises:
            ImageDirectoryNotSelected: If the current image directory is not selected.
        """
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            width, height = image.size
            new_width = int(width * width_percent / 100)
            new_height = int(height * height_percent / 100)
            image = image.resize((new_width, new_height))
            image.save(self.current_image_directory + 'resized.' + self.current_image_format)
        return self.current_image_directory + 'resized.' + self.current_image_format

    def grayscale_image(self):
        """
        Convert the current image to grayscale.

        Returns:
            str: The path to the grayscale image.

        Raises:
            ImageDirectoryNotSelected: If the current image directory is not selected.
        """
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            image = image.convert('L')
            image.save(self.current_image_directory + 'grayscaled.' + self.current_image_format)
        return self.current_image_directory + 'grayscaled.' + self.current_image_format

    def chanel_convert_image(self, chanel='r'):
        """
        Convert the current image to the specified color chanel.

        Args:
            chanel (str): The color chanel to convert the image to. Possible values are 'r', 'g', 'b'.

        Returns:
            str: The path to the image with the specified color chanel.

        Raises:
            UnknownMode: If the specified chanel is not 'r', 'g', or 'b'.
            ImageDirectoryNotSelected: If the current image directory is not selected.
        """
        if chanel != 'r' and chanel != 'g' and chanel != 'b':
            raise UnknownMode('Unknown chanel')
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            if self.current_image_format == 'png':
                image = image.convert('RGB')
            r, g, b = image.split()
            zeroes = r.point(lambda x: 0)
            chanel_image = Image.merge("RGB", (
                r if chanel == 'r' else zeroes,
                g if chanel == 'g' else zeroes,
                b if chanel == 'b' else zeroes
            ))
            chanel_image.save(self.current_image_directory + 'chanel_converted_' + chanel + '.' + self.current_image_format)
        return self.current_image_directory + 'chanel_converted_' + chanel + '.' + self.current_image_format

    def blur_image(self, blur_type='box', blur_radius=10):
        """
        Blur the current image with a specified blur type and radius.

        Args:
            blur_type (str, optional): The type of blur. Options are 'box' or 'gaussian'. Defaults to 'box'.
            blur_radius (int, optional): The radius of blur. Defaults to 10.

        Returns:
            str: The path to the blurred image.

        Raises:
            ImageDirectoryNotSelected: If the current image directory is not selected.
            UnknownMode: If the specified blur type is not 'box' or 'gaussian'.
        """
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        if blur_type != 'box' and blur_type != 'gaussian':
            raise UnknownMode('Unknown blur type')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            if self.current_image_format == 'png':
                image = image.convert('RGB')
            if blur_type == 'box':
                image = image.filter(ImageFilter.BoxBlur(radius=blur_radius))
            elif blur_type == 'gaussian':
                image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            image.save(self.current_image_directory + 'blurred.' + self.current_image_format)
        return self.current_image_directory + 'blurred.' + self.current_image_format

    def sharpen_image(self):
        """
        Sharpen the current image.

        Returns:
            str: The path to the sharpened image.

        Raises:
            ImageDirectoryNotSelected: If the current image directory is not selected.
        """
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            if self.current_image_format == 'png':
                image = image.convert('RGB')
            image = image.filter(ImageFilter.SHARPEN)
            image.save(self.current_image_directory + 'sharpened.' + self.current_image_format)
        return self.current_image_directory + 'sharpened.' + self.current_image_format

    def smooth_image(self):
        """
        Smooth the current image.

        Returns:
            str: The path to the smoothed image.

        Raises:
            ImageDirectoryNotSelected: If the current image directory is not selected.
        """
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            if self.current_image_format == 'png':
                image = image.convert('RGB')
            image = image.filter(ImageFilter.SMOOTH)
            image.save(self.current_image_directory + 'smoothed.' + self.current_image_format)
        return self.current_image_directory + 'smoothed.' + self.current_image_format

    def find_edges(self):
        """
        Find edges in the current image.

        Returns:
            str: The path to the image with found edges.

        Raises:
            ImageDirectoryNotSelected: If the current image directory is not selected.
        """
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            if self.current_image_format == 'png':
                image = image.convert('RGB')
            image = image.filter(ImageFilter.FIND_EDGES)
            image.save(self.current_image_directory + 'edges.' + self.current_image_format)
        return self.current_image_directory + 'edges.' + self.current_image_format

    def change_brightness(self, scale_value):
        """
        Adjust the brightness of the current image.

        Args:
            scale_value (float): The factor by which to adjust the brightness.
                                 Values greater than 1.0 increase brightness,
                                 while values between 0.0 and 1.0 decrease brightness.

        Returns:
            str: The path to the image with adjusted brightness.

        Raises:
            ImageDirectoryNotSelected: If the current image directory is not selected.
        """
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            if self.current_image_format == 'png':
                image = image.convert('RGB')
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(scale_value)
            image.save(self.current_image_directory + 'brightness_changed.' + self.current_image_format)
        return self.current_image_directory + 'brightness_changed.' + self.current_image_format

    def add_watermark(self, watermark_path, position_percentage=(0, 0)):
        """
        Add watermark to the image.

        Args:
            watermark_path (str): The path to the watermark image.
            position_percentage (tuple of int, optional): The position of the watermark in percentage of the image size.
                Defaults to (0, 0), which is the top left corner of the image.

        Returns:
            str: The path to the resulting image.

        Raises:
            ImageDirectoryNotSelected: If the current image directory is not selected.
        """
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            watermark = Image.open(watermark_path).convert("RGBA")
            image_width, image_height = image.size
            watermark_width, watermark_height = watermark.size
            x = int(image_width * position_percentage[0] / 100) - watermark_width
            y = int(image_height * position_percentage[1] / 100) - watermark_height
            image.paste(watermark, (x, y), watermark)
            image.save(self.current_image_directory + 'watermarked.' + self.current_image_format)
        return self.current_image_directory + 'watermarked.' + self.current_image_format

    def add_text(self, text, x=0, y=0, font_size=16, color=(0, 0, 0)):
        """
        Add a text to the image.

        Args:
            text (str): The text to add.
            x (int, optional): The x-coordinate of the text. Defaults to 0.
            y (int, optional): The y-coordinate of the text. Defaults to 0.
            font_size (int, optional): The font size of the text. Defaults to 16.
            color (tuple, optional): The color of the text. Defaults to (0, 0, 0).

        Returns:
            str: The path to the resulting image.

        Raises:
            ImageDirectoryNotSelected: If the current image directory is not selected.
        """
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            font = ImageFont.load_default()
            font = font.font_variant(size=font_size)
            draw = ImageDraw.Draw(image)
            draw.text((x, y), text, font=font, fill=color)
            image.save(self.current_image_directory + 'text_added.' + self.current_image_format)
        return self.current_image_directory + 'text_added.' + self.current_image_format

    def get_image_size(self):
        """
        Get the size of the image.

        Returns:
            tuple: A tuple (width, height) of the image size in pixels.

        Raises:
            ImageDirectoryNotSelected: If the current image directory is not selected.
        """
        if self.current_image_directory is None:
            raise ImageDirectoryNotSelected('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            return image.size


if __name__ == '__main__':
    formatter = ImageFormatter()

    # IMAGE_DIRECTORY = 'images/parsed_images'
    IMAGE_DIRECTORY = 'images/example_parsed_images'

    # U can choose any watermark image from images/static and even create your own at images/static
    WATERMARK_PATH = 'images/static/example_watermark.png'
    image_names = os.listdir(IMAGE_DIRECTORY)
    for image_name in image_names:
        try:
            formatter.select_image_directory(f'{IMAGE_DIRECTORY}/{image_name}/')
            formatter.rotate_image(90)
            formatter.flip_image('horizontal')
            formatter.crop_image(25, 25, 50, 50)
            formatter.resize_image(50, 50)
            formatter.grayscale_image()
            [formatter.chanel_convert_image(chanel) for chanel in ['r', 'g', 'b']]
            formatter.blur_image('box', 10)
            formatter.sharpen_image()
            formatter.smooth_image()
            formatter.find_edges()
            formatter.change_brightness(1.5)
            formatter.add_watermark(WATERMARK_PATH, (100, 100))
            formatter.add_text('Hello, world!', 0, 0, 32, (255, 0, 0))
        except UnknownMode as e:
            print(f'Image {image_name} - {e}')
        except ImageDirectoryNotSelected as e:
            print(f'Image {image_name} - {e}')
        except Exception as e:
            print(f'Image {image_name} - {e}')

