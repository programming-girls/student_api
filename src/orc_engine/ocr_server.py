from flask import Blueprint, request, Response, abort

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

ocr = Blueprint('ocr', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

@ocr.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return Response('No file selected')
        file = request.files['file']
        if file.filename == '':
            return abort(404),'No file selected'

        if file and allowed_file(file.filename):
            extracted_text = ocr_core(file)

            return Response(extracted_text)

