from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.travel_bot import Travel

# Khởi tạo Flask app
app = Flask(__name__)
CORS(app)  # Cho phép gọi từ React (localhost:3000)

# Khởi tạo agent du lịch (chỉ tạo 1 lần khi server khởi động)
travel_agent = Travel("gemini-2.0-flash", "google-genai", temperature=0)

# Route xử lý yêu cầu từ React
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message.strip():
            return jsonify({"reply": "Bạn chưa nhập gì cả!"})

        response = travel_agent.run(question=user_message)
        reply = response["output"]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Đã xảy ra lỗi: {str(e)}"}), 500

# Chạy server Flask
if __name__ == "__main__":
    app.run(debug=True)
