# ТЗ ИТА-ийн шилжилт хасах хүсэлтийн схем

**Description:** ТЗ-тэй ААНБ-аас ИТА хасах

- [1. Property `root > payload`](#payload)
  - [1.1. Property `root > payload > state`](#payload_state)
  - [1.2. Property `root > payload > license_id`](#payload_license_id)
  - [1.3. Property `root > payload > requirement_id`](#payload_requirement_id)
  - [1.4. Property `root > payload > regnum`](#payload_regnum)
  - [1.5. Property `root > payload > last_name`](#payload_last_name)
  - [1.6. Property `root > payload > first_name`](#payload_first_name)
  - [1.7. Property `root > payload > profession`](#payload_profession)
  - [1.8. Property `root > payload > degree`](#payload_degree)
  - [1.9. Property `root > payload > description`](#payload_description)
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

| Property                                     | Pattern | Type   | Deprecated | Definition | Title/Description                                                               |
| -------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------- |
| - [state](#payload_state )                   | No      | number | No         | -          | Блокчэйнд бичсэн эсэх төлөв. 0 бол бичээгүй, 1 бол бичсэн. 1 үед дахин бичихгүй |
| + [license_id](#payload_license_id )         | No      | string | No         | -          | ТЗ-ийн гэрчилгээний дугаар                                                      |
| + [requirement_id](#payload_requirement_id ) | No      | string | No         | -          | Заалтын дугаар                                                                  |
| + [regnum](#payload_regnum )                 | No      | string | No         | -          | ИТА-н Регистр                                                                   |
| + [last_name](#payload_last_name )           | No      | string | No         | -          | ИТА-н Эцэг/эх/-н нэр                                                            |
| + [first_name](#payload_first_name )         | No      | string | No         | -          | ИТА-н Өөрийн нэр                                                                |
| + [profession](#payload_profession )         | No      | string | No         | -          | ИТА-н Mэргэжил                                                                  |
| + [degree](#payload_degree )                 | No      | string | No         | -          | ИТА-н Mэргэшлийн зэрэг                                                          |
| + [description](#payload_description )       | No      | string | No         | -          | Тайлбар /нэмэлт мэдээлэл/                                                       |

### <a name="payload_state"></a>1.1. Property `root > payload > state`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | No       |
| **Default**  | `0`      |

**Description:** Блокчэйнд бичсэн эсэх төлөв. 0 бол бичээгүй, 1 бол бичсэн. 1 үед дахин бичихгүй

### <a name="payload_license_id"></a>1.2. Property `root > payload > license_id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** ТЗ-ийн гэрчилгээний дугаар

### <a name="payload_requirement_id"></a>1.3. Property `root > payload > requirement_id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Заалтын дугаар

### <a name="payload_regnum"></a>1.4. Property `root > payload > regnum`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** ИТА-н Регистр

### <a name="payload_last_name"></a>1.5. Property `root > payload > last_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** ИТА-н Эцэг/эх/-н нэр

### <a name="payload_first_name"></a>1.6. Property `root > payload > first_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** ИТА-н Өөрийн нэр

### <a name="payload_profession"></a>1.7. Property `root > payload > profession`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** ИТА-н Mэргэжил

### <a name="payload_degree"></a>1.8. Property `root > payload > degree`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** ИТА-н Mэргэшлийн зэрэг

### <a name="payload_description"></a>1.9. Property `root > payload > description`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Тайлбар /нэмэлт мэдээлэл/

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
