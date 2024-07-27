import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import film_simulation as fs
import json

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename.replace(' ',''))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Load film profiles from JSON
            # with open('film_profiles.json', 'r') as f:
            film_profiles = fs.load_film_profiles_from_json('film_profiles.json')

            output_files_with_labels = []
            for profile_name, profile in film_profiles.items():
                output_filename = f"{os.path.splitext(filename)[0]}_{profile_name.replace(' ', '_')}.jpg"
                output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

                # Process the image
                with Image.open(file_path) as img:
                    processed_image = fs.apply_film_profile(img, profile)
                    processed_image.save(output_file_path)

                # Append to output list
                output_files_with_labels.append((output_filename, profile_name))

            return render_template('index.html', filename=filename, output_files_with_labels=output_files_with_labels)

    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # app.run(debug=True, port=os.environ['PORT'], host='0.0.0.0')
    app.run(debug=True, port=6969)

# port=os.environ['PORT'], host='0.0.0.0'