# noinspection DuplicatedCode

RevokeSchema = {
  "type": "object",
  "description": "ТЗ цуцлах хүсэлтийн схем",
  "properties": {
    "payload": {
      "type": "object",
      "description": "Бүртгэх дата",
      "properties": {
        "license_id": {
          "type": "string",
          "description": "ТЗ-ийн гэрчилгээний дугаар"
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
      "required": [
        "license_id",
        "description"
      ]
    },
    "request_id": {
      "type": "string",
      "description": "Хүсэлтийн дугаар",
      "error_msg": "[request_id] оруулна уу."
    },
    "callback_url": {
      "type": "string",
      "description": "Хариу буцаах URL",
      "error_msg": "[callback_url] оруулна уу."
    }
  },
  "required": [
    "payload",
    "request_id",
    "callback_url"
  ]
}
