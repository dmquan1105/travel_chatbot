from dotenv import load_dotenv

load_dotenv(override=True)
import os
import requests
from langchain.tools import tool


@tool("get_weather")
def get_weather(location: str) -> str:
    """
    Lấy thông tin thời tiết hiện tại tại một địa điểm cụ thể.
    Args:
        location (str): Tên địa điểm cần lấy thông tin thời tiết.
    Returns:
        str: Thông tin thời tiết hiện tại, bao gồm trạng thái thời tiết, nhiệt độ, độ ẩm.
    """
    API_KEY = os.getenv("WEATHERAPI_KEY")
    if not API_KEY:
        return "API key cho WeatherAPI không được cấu hình. Vui lòng kiểm tra biến môi trường."

    # url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric&lang=vi"
    url = (
        f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}&lang=vi"
    )

    try:
        print("=" * 50)
        print("Using weather tool...")
        print("=" * 50)
        response = requests.get(url, timeout=5)
        data = response.json()

        if "error" in data:
            return f"Không lấy được thời tiết: {data['error'].get('message', 'Không rõ lỗi.')}"

        current = data["current"]
        location_data = data["location"]

        return {
            "location": location,
            "status": current["condition"]["text"],
            "temperature_c": current["temp_c"],
            "feels_like_c": current["feelslike_c"],
            "humidity": current["humidity"],
            "wind_kph": current["wind_kph"],
        }

    except Exception as e:
        return f"Lỗi khi gọi API thời tiết: {str(e)}"


def main():
    result = get_weather.invoke({"location": "Tam Đảo"})
    print(result)


if __name__ == "__main__":
    main()
