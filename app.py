# Import the module
from flask import Flask, render_template, request, jsonify
from pypinyin import pinyin

app = Flask(__name__)

# Routes to the specified url
@app.route("/")
def index():
	return render_template('index.html')

@app.route("/pinyin", methods=["POST"])
def get_pinyin():
	text = request.json["text"]
	result = pinyin(text)
	return jsonify(result)

# Special python nickname for the specific file you are executing
if __name__ == "__main__":
	app.run(debug=True);
