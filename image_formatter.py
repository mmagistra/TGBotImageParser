from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw
import os


class ImageFormatter:
    def __init__(self, default_path='images/parsed_images'):
        self.default_path = default_path
        self.current_image_directory = None
        self.current_image_format = None

        if not os.path.exists(self.default_path):
            os.makedirs(self.default_path)

    def select_image_directory(self, directory_path):
        if directory_path[-1] != '/':
            directory_path += '/'
        self.current_image_directory = directory_path
        for f in os.listdir(directory_path):
            if f.split('.')[0] == 'default':
                self.current_image_format = f.split('.')[-1]

        if self.current_image_format is None:
            raise Exception('Cannot find default image in directory')

    def rotate_image(self, angle):
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            image = image.rotate(angle)
            image.save(self.current_image_directory + 'rotated.' + self.current_image_format)
        return self.current_image_directory + 'rotated.' + self.current_image_format

    def flip_image(self, mode='horizontal'):
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

        if mode == 'horizontal':
            axis = Image.FLIP_LEFT_RIGHT
        elif mode == 'vertical':
            axis = Image.FLIP_TOP_BOTTOM
        else:
            raise Exception('Unknown flip mode')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            image = image.transpose(axis)
            image.save(self.current_image_directory + 'flipped_' + mode + '.' + self.current_image_format)
        return self.current_image_directory + 'flipped_' + mode + '.' + self.current_image_format

    def crop_image(self, x_percent, y_percent, width_percent, height_percent):
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

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
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            width, height = image.size
            new_width = int(width * width_percent / 100)
            new_height = int(height * height_percent / 100)
            image = image.resize((new_width, new_height))
            image.save(self.current_image_directory + 'resized.' + self.current_image_format)
        return self.current_image_directory + 'resized.' + self.current_image_format

    def grayscale_image(self):
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            image = image.convert('L')
            image.save(self.current_image_directory + 'grayscaled.' + self.current_image_format)
        return self.current_image_directory + 'grayscaled.' + self.current_image_format

    def chanel_convert_image(self, chanel='r'):
        if chanel != 'r' and chanel != 'g' and chanel != 'b':
            raise Exception('Unknown chanel')
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

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
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

        if blur_type != 'box' and blur_type != 'gaussian':
            raise Exception('Unknown blur type')

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
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            if self.current_image_format == 'png':
                image = image.convert('RGB')
            image = image.filter(ImageFilter.SHARPEN)
            image.save(self.current_image_directory + 'sharpened.' + self.current_image_format)
        return self.current_image_directory + 'sharpened.' + self.current_image_format

    def smooth_image(self):
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            if self.current_image_format == 'png':
                image = image.convert('RGB')
            image = image.filter(ImageFilter.SMOOTH)
            image.save(self.current_image_directory + 'smoothed.' + self.current_image_format)
        return self.current_image_directory + 'smoothed.' + self.current_image_format

    def find_edges(self):
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            if self.current_image_format == 'png':
                image = image.convert('RGB')
            image = image.filter(ImageFilter.FIND_EDGES)
            image.save(self.current_image_directory + 'edges.' + self.current_image_format)
        return self.current_image_directory + 'edges.' + self.current_image_format

    def change_brightness(self, scale_value):
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            if self.current_image_format == 'png':
                image = image.convert('RGB')
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(scale_value)
            image.save(self.current_image_directory + 'brightness_changed.' + self.current_image_format)
        return self.current_image_directory + 'brightness_changed.' + self.current_image_format

    def add_watermark(self, watermark_path, position_percentage=(0, 0)):
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

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
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            font = ImageFont.load_default()
            font = font.font_variant(size=font_size)
            draw = ImageDraw.Draw(image)
            draw.text((x, y), text, font=font, fill=color)
            image.save(self.current_image_directory + 'text_added.' + self.current_image_format)
        return self.current_image_directory + 'text_added.' + self.current_image_format

    def get_image_size(self):
        if self.current_image_directory is None:
            raise Exception('Current image directory is not selected')

        with Image.open(self.current_image_directory + 'default.' + self.current_image_format) as image:
            return image.size


if __name__ == '__main__':
    formatter = ImageFormatter()
    formatter.select_image_directory('images/example_parsed_images/source_link/image_name/')
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
    formatter.add_watermark('images/static/watermark.png', (100, 100))
    formatter.add_text('Hello, world!', 0, 0, 32, (255, 0, 0))

