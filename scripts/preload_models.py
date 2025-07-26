from transformers import AutoModel, AutoTokenizer


def preload():
    model_name = "VoVanPhuc/sup-SimCSE-VietNamese-phobert-base"
    print(f"Downloading model: {model_name}")
    AutoModel.from_pretrained(model_name)
    AutoTokenizer.from_pretrained(model_name)
    print("Model downloaded and cached.")


if __name__ == "__main__":
    preload()
