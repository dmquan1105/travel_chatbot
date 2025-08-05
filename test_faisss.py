from typing import Optional
from langchain_community.vectorstores import FAISS
from langchain.tools import tool
from travel_vectorstore.storage import TravelVectorStorage


@tool("search_travel_info")
def search_travel_info(query: str, location: Optional[str] = None) -> str:
    """
    Tìm kiếm thông tin du lịch từ cơ sở dữ liệu nội bộ.

    Sử dụng khi người dùng hỏi về địa điểm du lịch, địa danh nổi tiếng, nơi nên đi chơi, cảnh đẹp, nghỉ dưỡng, ẩm thực hoặc bất kỳ thông tin du lịch nào.

    Args:
        query (str): câu hỏi của người dùng
        location (Optional[str], optional): Địa điểm mà người dùng nhắc tới nếu có. Defaults to None.

    Returns:
        str: các đề xuất kết quả dựa trên truy vấn
    """
    print("=" * 50)
    print("Using search tool...")
    print("=" * 50)

    storage = TravelVectorStorage()
    storage.inspect(n=10) 
    results = storage.search(query=query, location=location)
    return "\n\n".join([doc.page_content for doc in results])


if __name__ == "__main__":
    query = "DI tích lịch sử ở Hà Nội"
    res = search_travel_info.invoke({"query": query, "location": "Hà Nội"})
    print(res)
