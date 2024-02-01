from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/save_rectangle', methods=['POST'])
def save_json():
    print("Received a request to save JSON data.")  # Diagnostic print
    data = request.json
    print(f"Data received: {data}")  # Print the data to see what's received
    try:
        with open('saved_data.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("File saved successfully.")  # Confirmation print
        return jsonify({"message": "Data saved successfully"})
    except Exception as e:
        print(f"Error saving file: {e}")  # Print any error encountered
        return jsonify({"error": "Failed to save data"}), 500

if __name__ == '__main__':
    app.run(debug=False)
