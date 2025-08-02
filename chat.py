from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import mysql.connector
import torch

# --- Flask Setup ---
app = Flask(__name__)
CORS(app)

# --- Load DialoGPT Model ---
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
chat_history_ids = None

# --- MySQL Config ---
db_config = {
    'user': 'root',
    'password': 'Aswin2005@',
    'host': 'localhost',
    'database': 'college_data'
}

# --- Department Aliases for NLP ---
department_keywords = {
    "CSE": ["cse", "computer science", "cs", "comp sci"],
    "IT": ["it", "information technology","iy"],
    "ECE": ["ece", "electronics", "electronics and communication"],
    "MECH": ["mech", "mechanical", "mechanical engineering"],
    "CIVIL": ["civil", "civil engineering"],
    "AI": ["ai", "artificial intelligence", "ai & ds", "ai and data science"]
}

# --- NLP: Extract Intent + Department ---
def extract_intent_and_department(user_input):
    input_lower = user_input.lower()
    intent = None
    department = None

    # Detect intent
    if any(word in input_lower for word in ["fee", "fees", "cost", "price"]):
        intent = "fees_structure"
    elif any(word in input_lower for word in ["eligibility", "requirement", "qualify", "criteria"]):
        intent = "eligibility_criteria"
    elif "scholarship" in input_lower or "scholarships" in input_lower:
        intent = "scholarships"

    # Detect department
    for dept_code, aliases in department_keywords.items():
        for alias in aliases:
            if alias in input_lower:
                department = dept_code
                break
        if department:
            break

    return intent, department

# --- SQL Query for College Info ---
def get_college_info(intent, department=None):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    query = f"SELECT name, {intent} FROM abc_college"
    if department:
        query += " WHERE name = %s"
        cursor.execute(query, (department,))
    else:
        cursor.execute(query)

    result = cursor.fetchall()
    cursor.close()
    connection.close()

    return format_info(result, intent)

# --- Format Response Nicely ---
def format_info(info, field):
    if not info:
        return "Sorry, I couldn't find any information."

    if len(info) == 1:
        dept = info[0]['name']
        value = info[0][field]
        if field == "fees_structure":
            return f"The fee for the {dept} department is ₹{int(value):,} per year."
        elif field == "eligibility_criteria":
            return f"The eligibility criteria for the {dept} department is: {value}"
        elif field == "scholarships":
            return f"The available scholarships for the {dept} department are: {value}"
    else:
        response = ""
        if field == "fees_structure":
            response += "Here are the fee details for all departments:\n"
            for entry in info:
                response += f"- {entry['name']}: ₹{int(entry[field]):,}/year\n"
        elif field == "eligibility_criteria":
            response += "Eligibility criteria for all departments:\n"
            for entry in info:
                response += f"- {entry['name']}: {entry[field]}\n"
        elif field == "scholarships":
            response += "Scholarships available in all departments:\n"
            for entry in info:
                response += f"- {entry['name']}: {entry[field]}\n"
        return response.strip()

# --- Main Chat Endpoint ---
@app.route("/chat", methods=["POST"])
def chat():
    global chat_history_ids
    data = request.json
    user_input = data.get("message", "")

    # NLP detection
    intent, department = extract_intent_and_department(user_input)

    # If it's a factual query, go to DB
    if intent:
        response = get_college_info(intent, department)
    else:
        # Otherwise, fall back to DialoGPT
        new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return jsonify({"response": response})

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)
