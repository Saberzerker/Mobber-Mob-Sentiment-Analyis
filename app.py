from flask import Flask, request, render_template
import os
from your_emotion_script import analyze_group_emotion_with_deepface
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    image_path = None
    group_faces_path = None
    spectrum_path = None  # Initialize spectrum_path to avoid UnboundLocalError

    if request.method == 'POST':
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(path)

            # Analyze the image and get both paths
            output_path, grouped_path, spectrum = analyze_group_emotion_with_deepface(path, 'model2.pth')

            # Assign the results to the initialized variables
            image_path = output_path
            group_faces_path = grouped_path
            spectrum_path = spectrum

    return render_template('index.html', image_path=image_path, group_faces_path=group_faces_path, spectrum_path=spectrum_path)

if __name__ == '__main__':
    app.run(debug=True)
