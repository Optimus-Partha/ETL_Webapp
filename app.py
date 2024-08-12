from flask import Flask, request, render_template, send_file
import pandas as pd
import io

app = Flask(__name__)


@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return "No file provided", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    df = pd.read_excel(file)

    # Perform ETL operations on DataFrame (example)
    df['new_column'] = df['existing_column'] * 2

    # Save the modified DataFrame to an Excel file
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)

    writer.close()  # Use close() instead of save()
    output.seek(0)

    return send_file(output, download_name='processed_file.xlsx', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
