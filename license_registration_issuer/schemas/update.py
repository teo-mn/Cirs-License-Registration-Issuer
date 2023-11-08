UpdateSchema = {
    "type": "object",
    "description": "ТЗ бүртгэх хүсэлтийн схем",
    "properties": {
        "payload": {
            "type": "object",
            "description": "Бүртгэх дата",
            "properties": {
                "license_system_id": {
                    "type": "string",
                    "description": "Тусгай зөвшөөрлийн системийн дугаар",
                },
                "license_id": {
                    "type": "string",
                    "description": "ТЗ-ийн гэрчилгээний дугаар",
                },
                "start_date": {
                    "type": "number",
                    "description": "ТЗ хүчинтэй хугацаа эхлэх огноо",
                },
                "end_date": {
                    "type": "number",
                    "description": "ТЗ хүчинтэй хугацаа дуусах огноо",
                },
                "owner_id": {
                    "type": "string",
                    "description": "Тусгай зөвшөөрөл эзэмшигч ААН -н регистр",
                },
                "owner_name": {
                    "type": "string",
                    "description": "Тусгай зөвшөөрөл эзэмшигч ААН -н нэр",
                },
                "description": {
                    "type": "string",
                    "description": "Тайлбар /нэмэлт мэдээлэл/"
                },
                "state": {
                    "type": "number",
                    "description": "Блокчэйнд бичсэн эсэх төлөв. 0 бол бичээгүй, 1 бол бичсэн. 1 үед дахин бичихгүй",
                    "default": 0
                }
            },
            "required": ["license_system_id", "license_id", "start_date", "end_date", "owner_id", "owner_name"]
        },
        "request_id": {
            "type": "string",
            "description": "request_id",
            "error_msg": "[request_id] оруулна уу."
        },
        "callback_url": {
            "type": "string",
            "description": "callback_url",
            "error_msg": "[callback_url] оруулна уу."
        }
    },
    "required": ["payload", "request_id", "callback_url"]
}
