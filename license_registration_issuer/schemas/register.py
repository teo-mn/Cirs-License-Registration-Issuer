RegisterSchema = {
  "type": "object",
  "description": "ТЗ бүртгэх хүсэлтийн схем",
  "properties": {
    "payload": {
      "type": "object",
      "description": "Бүртгэх дата",
      "properties": {
        "license_system_id": {
          "type": "string",
          "description": "Тусгай зөвшөөрлийн системийн дугаар"
        },
        "license_id": {
          "type": "string",
          "description": "ТЗ-ийн гэрчилгээний дугаар"
        },
        "license_type": {
          "type": "string",
          "description": "ТЗ-ийн төрөл. Жишээ: Барилга угсралт"
        },
        "start_date": {
          "type": "number",
          "description": "ТЗ хүчинтэй хугацаа эхлэх огноо"
        },
        "end_date": {
          "type": "number",
          "description": "ТЗ хүчинтэй хугацаа дуусах огноо"
        },
        "owner_id": {
          "type": "string",
          "description": "Тусгай зөвшөөрөл эзэмшигч ААН -н регистр"
        },
        "owner_name": {
          "type": "string",
          "description": "Тусгай зөвшөөрөл эзэмшигч ААН -н нэр"
        },
        "description": {
          "type": "string",
          "description": "Тайлбар /нэмэлт мэдээлэл/"
        },
        "state": {
          "type": "number",
          "description": "Блокчэйнд бичсэн эсэх төлөв. 0 бол бичээгүй, 1 бол бичсэн. 1 үед дахин бичихгүй",
          "default": 0
        },
        "requirements": {
          "type": "array",
          "description": "Заалтуудын мэдээллэл",
          "items": {
            "type": "object",
            "properties": {
              "requirement_system_id": {
                "type": "string",
                "description": "Хамаарах заалтын системийн дугаар"
              },
              "requirement_id": {
                "type": "string",
                "description": "Заалтын дугаар"
              },
              "employees": {
                "type": "array",
                "description": "ИТА мэдээллэл",
                "items": {
                  "type": "object",
                  "description": "",
                  "properties": {
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
                    "state": {
                      "type": "number",
                      "description": "Блокчэйнд бичсэн эсэх төлөв. 0 бол бичээгүй, 1 бол бичсэн. 1 үед дахин бичихгүй",
                      "default": 0
                    }
                  },
                  "required": [
                    "regnum",
                    "last_name",
                    "first_name",
                    "profession",
                    "degree"
                  ]
                }
              },
              "state": {
                "type": "number",
                "description": "Блокчэйнд бичсэн эсэх төлөв. 0 бол бичээгүй, 1 бол бичсэн. 1 үед дахин бичихгүй",
                "default": 0
              }
            },
            "required": [
              "requirement_system_id",
              "requirement_id",
              "employees"
            ]
          }
        }
      },
      "required": [
        "license_system_id",
        "license_id",
        "license_type",
        "start_date",
        "end_date",
        "owner_id",
        "owner_name",
        "requirements"
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
