import os
from typing import List, Optional, Dict

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from travel_vectorstore.loader import load_documents_from_jsonl
from utils.common import singleton
from langchain_text_splitters import RecursiveCharacterTextSplitter

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


@singleton
class TravelVectorStorage(object):
    def __init__(self, cache: str = f"{ROOT_PATH}/faiss_cache", reset: bool = False):
        self.vectorstore = None
        self.embedding = HuggingFaceEmbeddings(
            model_name="VoVanPhuc/sup-SimCSE-VietNamese-phobert-base"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300, chunk_overlap=50, separators=["\n\n", "\n", "."]
        )

        if reset and os.path.exists(cache):
            import shutil

            shutil.rmtree(cache)

        os.makedirs(cache, exist_ok=True)

        self.cache_path = cache
        self.index_file = os.path.join(cache, "index.faiss")
        self.pkl_file = os.path.join(cache, "index.pkl")

        if (
            os.path.exists(self.index_file)
            and os.path.exists(self.pkl_file)
            and not reset
        ):
            print("Loading FAISS vectorstore from cache...")
            self.vectorstore = FAISS.load_local(
                cache, self.embedding, allow_dangerous_deserialization=True
            )
        else:
            print("Building new FAISS vectorstore from JSONL...")
            docs = load_documents_from_jsonl("data/travel_data.jsonl")
            split_docs = self.text_splitter.split_documents(docs)
            self.vectorstore = FAISS.from_documents(split_docs, self.embedding)
            self.vectorstore.save_local(cache)

    def search(
        self, query: str, k: int = 40, location: Optional[str] = None
    ) -> List[Document]:
        """Finding relevant travel info, optionally filtered by location.

        Args:
            query (str): user query
            k (int, optional): top-k results. Defaults to 40.
            location (Optional[str], optional): Location filter. Defaults to None.

        Returns:
            List[Document]: Relevant documents
        """
        results = self.vectorstore.similarity_search(query, k=k)

        if location:
            filtered = [
                doc
                for doc in results
                if doc.metadata.get("location").lower() == location.lower()
            ]
            return filtered

        return results