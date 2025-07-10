from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.tools import tool
from utils.embedding import get_vectorstore


@tool("search_travel_info")
def search_travel_info(query: str) -> str:
    """
    Tìm kiếm thông tin du lịch từ cơ sở dữ liệu nội bộ.

    Sử dụng khi người dùng hỏi về địa điểm du lịch, địa danh nổi tiếng, nơi nên đi chơi, cảnh đẹp, nghỉ dưỡng, ẩm thực hoặc bất kỳ thông tin du lịch nào.
    """
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=3)
    return "\n\n".join([doc.page_content for doc in results])
