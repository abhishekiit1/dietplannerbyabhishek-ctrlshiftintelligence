from flask import Flask, render_template, request
from mira_sdk import MiraClient, Flow
import markdown

app = Flask(__name__)
client = MiraClient(config={"API_KEY": "sb-2f74348529988ddf72038b45bd4f50da"})
version = "1.0.0"
FLOW_ID = "dietplanner"

def execute_flow(age, weight, height, goal, diet_preference):
    input_data = {
        "age": int(age),
        "goal": goal,
        "height": int(height),
        "weight": float(weight),
        "diet_preference": diet_preference
    }
    if version:
        flow_name = f"@abhishekchaubey/dietplanner/{version}"
    else:
        flow_name = "@abhishekchaubey/dietplanner"
    
    result = client.flow.execute(flow_name, input_data)
    return result

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            age = request.form.get("age")
            weight = request.form.get("weight")
            height = request.form.get("height")
            goal = request.form.get("goal")
            diet_preference = request.form.get("diet_preference")
            result = execute_flow(age, weight, height, goal, diet_preference)
            if result is None:
                return "No diet plan generated. Please try again.", 400
            
            raw_text = result.get("result", "") if isinstance(result, dict) else str(result)
            processed_text = raw_text.replace("\\n", "\n")
            formatted_html = markdown.markdown(processed_text)
            return render_template("result.html", plan=formatted_html)
        except Exception as e:
            return f"Error processing form: {str(e)}", 400
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
