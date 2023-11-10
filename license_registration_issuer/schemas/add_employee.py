# noinspection DuplicatedCode

AddEmployeeSchema = {
  "type": "object",
  "description": "ТЗ-тэй ААНБ-ын хасагдсан заалтан дээр орлуулах ИТА",
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
        "regnum": {
          "type": "string",
          "description": "ИТА-н Регистр"
        },
        "last_name": {
          "type": "string",
          "description": "ИТА-н Эцэг/эх/-н нэр"
        },
        "first_name": {
          "type": "string",
          "description": "ИТА-н Өөрийн нэр"
        },
        "profession": {
          "type": "string",
          "description": "ИТА-н Mэргэжил"
        },
        "degree": {
          "type": "string",
          "description": "ИТА-н Mэргэшлийн зэрэг"
        },
        "description": {
          "type": "string",
          "description": "Тайлбар /Орлох хүсэлтийн системийн дугаар/"
        }
      },
      "required": [
        "license_id",
        "requirement_id",
        "regnum",
        "last_name",
        "first_name",
        "profession",
        "degree",
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
