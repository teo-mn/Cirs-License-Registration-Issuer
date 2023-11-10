# ТЗ сунгалт хийх хүсэлтийн схем


**Description:** Тусгай зөвшөөрлийн сунгалт /Хүчинтэй хугацаа сунгах/

- [1. Property `root > payload`](#payload)
  - [1.1. Property `root > payload > license_system_id`](#payload_license_system_id)
  - [1.2. Property `root > payload > license_id`](#payload_license_id)
  - [1.3. Property `root > payload > start_date`](#payload_start_date)
  - [1.4. Property `root > payload > end_date`](#payload_end_date)
  - [1.5. Property `root > payload > owner_id`](#payload_owner_id)
  - [1.6. Property `root > payload > owner_name`](#payload_owner_name)
  - [1.7. Property `root > payload > description`](#payload_description)
  - [1.8. Property `root > payload > state`](#payload_state)
- [2. Property `root > request_id`](#request_id)
- [3. Property `root > callback_url`](#callback_url)

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                        |

| Property                         | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [payload](#payload )           | No      | object | No         | -          | Бүртгэх дата      |
| + [request_id](#request_id )     | No      | string | No         | -          | request_id        |
| + [callback_url](#callback_url ) | No      | string | No         | -          | callback_url      |

## <a name="payload"></a>1. Property `root > payload`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |

**Description:** Бүртгэх дата

| Property                                           | Pattern | Type   | Deprecated | Definition | Title/Description                                                               |
| -------------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------- |
| + [license_system_id](#payload_license_system_id ) | No      | string | No         | -          | Тусгай зөвшөөрлийн системийн дугаар                                             |
| + [license_id](#payload_license_id )               | No      | string | No         | -          | ТЗ-ийн гэрчилгээний дугаар                                                      |
| + [start_date](#payload_start_date )               | No      | number | No         | -          | ТЗ хүчинтэй хугацаа эхлэх огноо                                                 |
| + [end_date](#payload_end_date )                   | No      | number | No         | -          | ТЗ хүчинтэй хугацаа дуусах огноо                                                |
| + [owner_id](#payload_owner_id )                   | No      | string | No         | -          | Тусгай зөвшөөрөл эзэмшигч ААН -н регистр                                        |
| + [owner_name](#payload_owner_name )               | No      | string | No         | -          | Тусгай зөвшөөрөл эзэмшигч ААН -н нэр                                            |
| - [description](#payload_description )             | No      | string | No         | -          | Тайлбар /нэмэлт мэдээлэл/                                                       |
| - [state](#payload_state )                         | No      | number | No         | -          | Блокчэйнд бичсэн эсэх төлөв. 0 бол бичээгүй, 1 бол бичсэн. 1 үед дахин бичихгүй |

### <a name="payload_license_system_id"></a>1.1. Property `root > payload > license_system_id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Тусгай зөвшөөрлийн системийн дугаар

### <a name="payload_license_id"></a>1.2. Property `root > payload > license_id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** ТЗ-ийн гэрчилгээний дугаар

### <a name="payload_start_date"></a>1.3. Property `root > payload > start_date`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** ТЗ хүчинтэй хугацаа эхлэх огноо

### <a name="payload_end_date"></a>1.4. Property `root > payload > end_date`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** ТЗ хүчинтэй хугацаа дуусах огноо

### <a name="payload_owner_id"></a>1.5. Property `root > payload > owner_id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Тусгай зөвшөөрөл эзэмшигч ААН -н регистр

### <a name="payload_owner_name"></a>1.6. Property `root > payload > owner_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Тусгай зөвшөөрөл эзэмшигч ААН -н нэр

### <a name="payload_description"></a>1.7. Property `root > payload > description`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Тайлбар /нэмэлт мэдээлэл/

### <a name="payload_state"></a>1.8. Property `root > payload > state`

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

**Description:** request_id

## <a name="callback_url"></a>3. Property `root > callback_url`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** callback_url

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2023-11-10 at 11:06:09 +0800
