import pandas as pd
import io
import json
# The key change is replacing render_template_string with render_template
from flask import Flask, request, send_file, render_template

# Import the functions from your converters file
import converters

app = Flask(__name__)

# This route now uses a dedicated HTML file
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        converter_choice = request.form.get('converter_type')

        if not file or file.filename == '':
            return 'No selected file', 400

        if file and file.filename.endswith('.json'):
            try:
                data = json.load(file.stream)
                df_final = None

                if converter_choice == 'globosat_composite':
                    df_final = converters.convert_globosat_composite(data)
                elif converter_choice == 'globosat_planning':
                    df_final = converters.convert_globosat_planning(data)
                elif converter_choice == 'fuboln':
                    df_final = converters.convert_fuboln(data)
                elif converter_choice == 'generic':
                    df_final = converters.convert_generic(data)
                else:
                    return "Invalid converter type selected", 400
                
                output = io.BytesIO()
                df_final.to_excel(output, index=False, sheet_name='Sheet1')
                output.seek(0)

                download_name = f"converted_{converter_choice}.xlsx"
                return send_file(
                    output,
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name=download_name
                )
            except Exception as e:
                return f"An error occurred: {e}", 500
    
    # For GET requests, render the HTML file from the 'templates' folder
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)