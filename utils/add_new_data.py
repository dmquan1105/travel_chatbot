import json
from typing import Optional


def append_to_jsonl_file(
    content: str,
    location: Optional[str] = None,
    file_path: str = "data/travel_data.jsonl",
):
    # Build dictionary từ input
    data = {"content": content, "location": None}
    if location:
        data["location"] = location

    # Thay \n trong chuỗi bằng \\n để giữ 1 dòng JSON
    def escape_newlines(obj):
        if isinstance(obj, dict):
            return {k: escape_newlines(v) for k, v in obj.items()}
        elif isinstance(obj, str):
            return obj.replace("\n", "\\n")
        else:
            return obj

    escaped_data = escape_newlines(data)

    # Ghi vào file JSONL
    with open(file_path, "a", encoding="utf-8") as f:
        json_line = json.dumps(escaped_data, ensure_ascii=False)
        f.write(json_line + "\n")


def main():
    append_to_jsonl_file(
        content="""Giáp Văn Hải, hướng dẫn viên du lịch ở Hà Giang, cho hay mùa hoa tam giác mạch được nhiều du khách mong đợi nhất khi tới Hà Giang. Tháng 11, đường lên Hà Giang đã thuận tiện, hoa đã bắt đầu chớm nở trên những nương đá, ruộng bậc thang. Hoa sẽ nở rộ đẹp nhất trong tháng 11 kéo dài sang đầu tháng 12.

"Đến Hà Giang lúc này là đẹp nhất, thời tiết 'chiều lòng người'", anh Hải nói. Những ngày đầu tháng 11, ban ngày nhiệt độ 18-23 độ, trời nắng, buổi tối khoảng 13-18 độ, chưa quá lạnh, khô ráo.

Hướng dẫn viên cũng nói thêm hoa tam giác mạch giờ không còn khó "săn" như trước kia vì hoa đã được nhân giống và trồng ở mọi nơi, dù trái mùa nhiều nơi vẫn có hoa. "Nhưng nếu nở chính vụ hoa tam giác mạch sẽ thắm hơn, cây cao và đẹp hơn", anh Hải nói.

Anh Hải gợi ý một số điểm ngắm hoa tam giác mạch phổ biến dành cho khách du lịch như dọc Quốc lộ 4C có các điểm Thạch Sơn Thần, Tam Sơn Quản Bạ - Vần Chải, Phố Cáo, Nhà Pao, Lũng Táo, Sán Trồ (đường vào Lũng Cú). Ngoài ra, nếu có nhiều thời gian và thích lang thang vào các bản làng trên cao nguyên đá, du khách có thể ghé qua Lao Xa, Phố Bảng, Phố Là. Ở đây có nhiều cánh đồng tam giác mạnh trồng tự nhiên, ít khai thác du lịch.

Bên cạnh tam giác mạch, anh Hải cho hay còn có hoa cúc cam dại cũng bắt đầu vào mùa. Đây là loài hoa đại diện cho con người vùng cao "mạnh mẽ vươn lên cứng cỏi mọc và nở trên đá". Hết mùa tam giác mạch, Hà Giang sẽ vào mùa hoa mơ, hoa mận, hoa đào.

""",
        location="Hà Giang",
    )


if __name__ == "__main__":
    main()
