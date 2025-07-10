from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from travel_vectorstore.build_vectorstore import build_vectorstore
import os

_embedding = None
_vectorstore = None


def get_embedding_model():
    global _embedding
    if _embedding is None:
        _embedding = HuggingFaceEmbeddings(
            model_name="VoVanPhuc/sup-SimCSE-VietNamese-phobert-base"
        )
    return _embedding


def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        faiss_folder = "travel_vectorstore"
        faiss_index = os.path.join(faiss_folder, "index.faiss")
        faiss_pkl = os.path.join(faiss_folder, "index.pkl")

        if not (os.path.exists(faiss_index) and os.path.exists(faiss_pkl)):
            print("FAISS not found. Building new vectorstore...")
            build_vectorstore()

        print("Loading FAISS vectorstore...")
        embedding_model = get_embedding_model()
        _vectorstore = FAISS.load_local(
            faiss_folder, embedding_model, allow_dangerous_deserialization=True
        )

    return _vectorstore
