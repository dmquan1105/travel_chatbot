from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document


def build_vectorstore():
    embedding_model = HuggingFaceEmbeddings(
        model_name="VoVanPhuc/sup-SimCSE-VietNamese-phobert-base"
    )

    docs = [
        Document(
            page_content="Thái Bình có đền Trần là di tích lịch sử nổi tiếng, được nhiều người biết đến."
        ),
        Document(
            page_content="Hồ Tây, Hà Nội là nơi lý tưởng để các bạn trẻ đi 'chill'."
        ),
        Document(
            page_content="Đà Lạt nổi tiếng với khí hậu mát mẻ quanh năm, đồi thông và các vườn hoa rực rỡ."
        ),
        Document(
            page_content="Hội An là phố cổ với đèn lồng lung linh, kiến trúc cổ kính và ẩm thực đa dạng."
        ),
        Document(
            page_content="Vịnh Hạ Long là di sản thiên nhiên thế giới với hàng ngàn hòn đảo đá vôi giữa biển."
        ),
        Document(
            page_content="Nha Trang có bãi biển dài, nước trong xanh và nhiều khu nghỉ dưỡng cao cấp."
        ),
        Document(
            page_content="Phú Quốc là hòn đảo nổi tiếng với biển xanh, cát trắng, và các resort sang trọng."
        ),
        Document(
            page_content="Sapa có ruộng bậc thang, bản làng dân tộc thiểu số và đỉnh Fansipan."
        ),
        Document(
            page_content="Cần Thơ nổi tiếng với chợ nổi Cái Răng và văn hóa miền sông nước."
        ),
        Document(
            page_content="Huế là thành phố cổ kính với Đại Nội, lăng tẩm vua chúa và sông Hương thơ mộng."
        ),
        Document(
            page_content="Đà Nẵng có bãi biển Mỹ Khê, Cầu Rồng phun lửa và Bà Nà Hills."
        ),
        Document(
            page_content="Mộc Châu nổi tiếng với hoa cải trắng, đồi chè và khí hậu mát mẻ."
        ),
        Document(
            page_content="Tam Đảo là điểm nghỉ dưỡng gần Hà Nội với không khí trong lành và nhiều villa đẹp."
        ),
        Document(
            page_content="Biển Cửa Lò ở Nghệ An là nơi nghỉ mát phổ biến vào mùa hè."
        ),
        Document(
            page_content="Chùa Bái Đính ở Ninh Bình là quần thể chùa lớn nhất Đông Nam Á."
        ),
        Document(
            page_content="Tràng An có hệ thống hang động và sông nước đẹp mê hồn, từng là bối cảnh phim Kong."
        ),
    ]

    vectorstore = FAISS.from_documents(docs, embedding=embedding_model)
    vectorstore.save_local("travel_vectorstore")
