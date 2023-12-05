# noinspection DuplicatedCode

RemoveRequirementSchema = {
  "type": "object",
  "description": "Заалт хасах хүсэлтийн схем",
  "properties": {
    "payload": {
      "type": "object",
      "description": "Бүртгэх дата",
      "properties": {
        "state": {
          "type": "number",
          "description": "Блокчэйнд бичсэн эсэх төлөв. 0 бол бичээгүй, 1 бол бичсэн. 1 үед дахин бичихгүй",
          "default": 0
        },
        "license_id": {
          "type": "string",
          "description": "ТЗ-ийн гэрчилгээний дугаар"
        },
        "requirement_id": {
          "type": "string",
          "description": "Заалтын дугаар"
        },
        "description": {
          "type": "string",
          "description": "Тайлбар /нэмэлт мэдээлэл/"
        },
      },
      "required": [
        "license_id",
        "requirement_id",
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
