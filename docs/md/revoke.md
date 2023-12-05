# ТЗ хүчингүй болгох

**Description:** ТЗ цуцлах хүсэлтийн схем

- [1. Property `root > payload`](#payload)
  - [1.1. Property `root > payload > license_id`](#payload_license_id)
  - [1.2. Property `root > payload > description`](#payload_description)
  - [1.3. Property `root > payload > state`](#payload_state)
- [2. Property `root > request_id`](#request_id)
- [3. Property `root > callback_url`](#callback_url)

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |


| Property                         | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [payload](#payload )           | No      | object | No         | -          | Бүртгэх дата      |
| + [request_id](#request_id )     | No      | string | No         | -          | Хүсэлтийн дугаар  |
| + [callback_url](#callback_url ) | No      | string | No         | -          | Хариу буцаах URL  |

## <a name="payload"></a>1. Property `root > payload`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** Бүртгэх дата

| Property                               | Pattern | Type   | Deprecated | Definition | Title/Description                                                               |
| -------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------- |
| + [license_id](#payload_license_id )   | No      | string | No         | -          | ТЗ-ийн гэрчилгээний дугаар                                                      |
| + [description](#payload_description ) | No      | string | No         | -          | Тайлбар /нэмэлт мэдээлэл/                                                       |
| - [state](#payload_state )             | No      | number | No         | -          | Блокчэйнд бичсэн эсэх төлөв. 0 бол бичээгүй, 1 бол бичсэн. 1 үед дахин бичихгүй |

### <a name="payload_license_id"></a>1.1. Property `root > payload > license_id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** ТЗ-ийн гэрчилгээний дугаар

### <a name="payload_description"></a>1.2. Property `root > payload > description`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Тайлбар /нэмэлт мэдээлэл/

### <a name="payload_state"></a>1.3. Property `root > payload > state`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0`      |

**Description:** Блокчэйнд бичсэн эсэх төлөв. 0 бол бичээгүй, 1 бол бичсэн. 1 үед дахин бичихгүй

## <a name="request_id"></a>2. Property `root > request_id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Хүсэлтийн дугаар

## <a name="callback_url"></a>3. Property `root > callback_url`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Хариу буцаах URL

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2023-12-05 at 12:04:37 +0800
