# Travel Chatbot

Một chatbot du lịch thông minh sử dụng LangChain và Gemini AI để cung cấp thông tin du lịch, thời tiết và lên kế hoạch cho chuyến đi.

## Tính năng

- **Tìm kiếm thông tin du lịch**: Tìm kiếm địa điểm, ẩm thực, lịch sử từ cơ sở dữ liệu.
- **Thông tin thời tiết**: Lấy thông tin thời tiết real-time.
- **Tìm kiếm web**: Tìm kiếm thông tin mới nhất từ internet.
- **Lập kế hoạch du lịch**: Tự động lên kế hoạch chi tiết cho chuyến đi.
- **Giao diện web**: Frontend hiện đại với React.

## Yêu cầu hệ thống

- Python 3.8+
- Node.js 16+ (cho frontend)
- RAM: tối thiểu 4GB (khuyến nghị 8GB)

## Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/dmquan1105/travel_chatbot.git
cd travel_chatbot
```

### 2. Tạo virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

### 3. Cài dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình environment variables

Tạo file `.env` dựa trên `.env.example`:

```bash
cp .env.example .env
```

Điền các API cần thiết:

```bash
# Google Gemini API
GOOGLE_API_KEY=<your_gemini_api_key>

# Weather API
WEATHERAPI_KEY=<your_weather_api_key>

# Tavily Search API
TAVILY_API_KEY=<your_tavily_api_key>

# Tạo database ở Mongodb atlas
MONGO_URI=<your_mongo_url>
```

### 5. Preload models

```bash
python -m scripts.preload_models
```

## API Keys

### Google Gemini API

Truy cập Google AI Studio
Tạo API key
Thêm vào file `.env`

### Weather API

Đăng ký tại WeatherAPI.com
Lấy API key từ tab API
Thêm WEATHERAPI_KEY vào `.env`

### Tavily Search API

Đăng ký tại Tavily
Lấy API key
Thêm TAVILY_API_KEY vào `.env`

## Chạy ứng dụng

### 1. Run frontend

```bash
cd frontend
npm install
npm run dev
```

### 2. Run backend

```bash
cd backend
uvicorn server:app --reload --port 5001
```
