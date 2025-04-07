# MCP-Armonia

ARA Protocol

| **Project:** | Armonía |
| --- | --- |
| **Function Area:** |  |
| **Title:** | Armonia Remote API Protocol |
| **Doc. Id:** |  |
| **Issue:** | 1.0.3 |
| **Date:** | 05/02/2018 |

| Author(s) |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Name(s): | Alessio Carello | Role: | Software Developer | Signature & Date: |  |
| Name(s): |  | Role: |  | Signature & Date: |  |
| Name(s): |  | Role: |  | Signature & Date: |  |

| Approved by |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Name(s): |  | Role: |  | Signature & Date: |  |
| Name(s): |  | Role: |  | Signature & Date: |  |
| Name(s): |  | Role: |  | Signature & Date: |  |

Revision History

| Version | Date | Updated by | Changes |
| --- | --- | --- | --- |
| 1.0.0 | 02/03/2018 | A. Carello | First edition |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
1. [Overview........................................................................................................................................... 4](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)
2. [Authentication................................................................................................................................... 4](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)
3. [Errors Code....................................................................................................................................... 5](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)
4. [API.................................................................................................................................................... 5](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.1. GetSystemStatus........................................................................................................................ 6](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.1.1. GetSystemStatus Example.................................................................................................. 7](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.2. SetAdvancedEqGain.................................................................................................................. 8](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.2.1. SetAdvancedEqGain Example........................................................................................... 9](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.3. SetAdvancedEqDelay.............................................................................................................. 10](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.3.1. SetAdvancedEqDelay Example........................................................................................ 11](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.4. SetSpeakerEqFIR..................................................................................................................... 12](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.4.1. SetSpeakerEqFIR Example.............................................................................................. 13](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.5. SetOutputEqFIR...................................................................................................................... 14](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.5.1. SetOutputEqFIR Example................................................................................................ 15](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.6. SetOutputEqGain..................................................................................................................... 16](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.6.1. SetOutputEqGain Example............................................................................................... 17](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.7. SetOutputEqPhase................................................................................................................... 18](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.7.1. SetOutputEqPhase Example............................................................................................. 19](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.8. CreateAndAssignGroup........................................................................................................... 20](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.8.1. CreateAndAssignGroup Example.................................................................................... 21](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.9. UnassignGroup........................................................................................................................ 22](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.9.1. UnassignGroup Example.................................................................................................. 23](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.10. OpenEntityDetails.................................................................................................................. 24](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

[4.10.1. OpenEntityDetails Example........................................................................................... 25](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md)

# 1. Overview

This document describes the API exposed by Armonia to let the control the status of the device available in the system.

Armonia listen to the port 40402 exposing a REST Web API with JSON payload.

The HTTP Status Code is used to describe the error\status of the request(an error code and description are provided also when necessary).

All fields are in PascalCase. The Id field and Ip are in UpperCase, so Id is ID (eg. UniqueID).

This example is a json response given from the [GetSystemStatus](MCP-Armonia%201cba8d6b84b880d2b24ade523da3433d.md) request.

[HTTP STATUS: 200]

{

"Devices": [

{

"IpAddress": "192.168.1.10",

"Name": "Device1",

"Serial": "1234",

"Model": "Model_1",

"UniqueID": "Model_1_1234",

"IsLinked": true,

"IsOnline": true,

"FirmwareVersion": "1.0.0.0"

}

],

"ERROR_CODE": null,

"ERROR_DESCRIPTION": null

}

# 2. Authentication

Armonía requires a valid token to reply to requests. This is necessary to ensure that request comes from a safe source.

The authentication information must be provided in the request header. In particular the following field must be filled with a valid token:

authClientToken: token-given-by-powersoft

If you don't provide this token, an HTTP Status Code 401 (unauhtorized) will be provided.

# 3. Errors Code

When a request to Armonía contains wrong informations or tries to do an invalid operation the HTTP Status Code will be accompanied by an error code plus a human readable description.

Actually Armonía provide the following error codes plus a human readable description. The error code can be used by a software, error description can be used by a programmer to understand the problem. The description will be populate with the most accurate problem description:

| ERROR_CODE | ERROR_DESCRIPTION (examples) |
| --- | --- |
| **ERROR_GENERIC** | *Generic Error* |
| **ERROR_REQUEST_NOT_IMPLEMENTED** | *This request is not implemented by ARA* |
| **ERROR_PROTECTED_KEY_NOT_CONFIGURATED** | *Protected key resource not configurated. Please check the system configuration.* |
| **ERROR_RESOURCE_KEY_HEADER_NOT_FOUND** | *Resource key header not found in HTTP context stream* |
| **ERROR_RESOURCE_KEY_HEADER_NOT_VALID** | *Resource key header value not valid in HTTP context stream* |
| **ERROR_NULL_REQUEST_PARAMETER** | *The request object can not be null* |
| **ERROR_IP_NOT_VALID** | *Ip not valid* |
| **ERROR_CHANNEL_NOT_VALID** | *Channel not valid* |
| **ERROR_ENTITY_NOT_FOUND** | *Entity not found* |
| **ERROR_VALUE_NOT_VALID** | *Value not valid* |

# 4. API

The APIs are reachable at http://<armoniasmachineip>:40402/api/ARA/<apiname>

| **API** | **4.1.     GetSystemStatus** |
| --- | --- |
| **Type** | **GET** |
| **Description** | Through this command the client asks for the system status. |
| **Parameters** | **Identifier** |
|  | - |
| **RESPONSE** |  |
| **Status Code** | 200 OK, 400 Bad Request, 401 Unauthorized |
| **Parameters** | **Identifier** |
| **1** | Devices |
|  | ERROR_CODE |
|  | ERROR_DESCRIPTION |

### 4.1.1. GetSystemStatus Example

**Endpoint**

GET /api/ARA/GetSystemStatus HTTP/1.1

**Header**

authClientToken: fcb0d2ee-9179-4968-8799-690fd242d530

**Body**

**Response**

{

"Devices": [

{

"IPAddress": "169.254.54.28",

"Name": null,

"SerialNumber": "00279465",

"Model": "DM 948 DSP+D",

"UniqueID": "DQ4804-4804_00279465",

"IsLinked": true,

"IsOnline": true,

"FirmwareVersion": "1.8.6.35"

},

{

"IPAddress": "",

"Name": null,

"SerialNumber": null,

"Model": "DM 912 DSP+D",

"UniqueID": "DQ1204-2404_dac761bd-6244-4543-8bee-cca362dcc31d",

"IsLinked": false,

"IsOnline": false,

"FirmwareVersion": "0.0.0.0"

},

{

"IPAddress": "",

"Name": null,

"SerialNumber": null,

"Model": "DM 924 DSP+D",

"UniqueID": "DQ2404-2404_f14a8bd8-e134-439c-882e-5621cef5bf6d",

"IsLinked": false,

"IsOnline": false,

"FirmwareVersion": "0.0.0.0"

}

],

"ERROR_CODE": null,

"ERROR_DESCRIPTION": null

}

| **API** | **4.2.     SetAdvancedEqGain** |
| --- | --- |
| **Type** | **POST** |
| **Description** | Through this command the client set the gain of Advanced EQ. |
| **Parameters** | **Identifier** |
| **1** | UniqueID |
| **2** | Value |
| **3** | Channel |
| **RESPONSE** |  |
| **Status Code** | 200 OK, 400 Bad Request, 401 Unauthorized |
| **Parameters** | **Identifier** |
|  | ERROR_CODE |
|  | ERROR_DESCRIPTION |

### 4.2.1. SetAdvancedEqGain Example

**Endpoint**

POST /api/ARA/SetAdvancedEqGain HTTP/1.1

**Header**

authClientToken: fcb0d2ee-9179-4968-8799-690fd242d530

**Body**

{     "UniqueID": "DQ4804-4804_00279465",     "Value": “5.6”,     "Channel": “0”,}

**Response → Status 200**

{

"ERROR_CODE": null,

"ERROR_DESCRIPTION": null

}

| **API** | **4.3.     SetAdvancedEqDelay** |
| --- | --- |
| **Type** | **POST** |
| **Description** | Through this command the client set the delay of Advanced EQ. |
| **Parameters** | **Identifier** |
| **1** | UniqueID |
| **2** | Value |
| **3** | Channel |
| **RESPONSE** |  |
| **Status Code** | 200 OK, 400 Bad Request, 401 Unauthorized |
| **Parameters** | **Identifier** |
|  | ERROR_CODE |
|  | ERROR_DESCRIPTION |

### 4.3.1. SetAdvancedEqDelay Example

**Endpoint**

POST /api/ARA/SetAdvancedEqDelay HTTP/1.1

**Header**

authClientToken: fcb0d2ee-9179-4968-8799-690fd242d530

**Body**

{     "UniqueID": "DQ4804-4804_00279465",     "Value": “50”,     "Channel": “0”,}

**Response → Status 200**

{

"ERROR_CODE": null,

"ERROR_DESCRIPTION": null

}

| **API** | **4.4.     SetSpeakerEqFIR** |
| --- | --- |
| **Type** | **POST** |
| **Description** | Through this command the client set the Speaker EQ FIR. |
| **Parameters** | **Identifier** |
| **1** | UniqueID |
| **2** | Values |
| **3** | Channel |
| **RESPONSE** |  |
| **Status Code** | 200 OK, 400 Bad Request, 401 Unauthorized |
| **Parameters** | **Identifier** |
|  | ERROR_CODE |
|  | ERROR_DESCRIPTION |

### 4.4.1. SetSpeakerEqFIR Example

**Endpoint**

POST /api/ARA/SetSpeakerEqFIR HTTP/1.1

**Header**

authClientToken: fcb0d2ee-9179-4968-8799-690fd242d530

**Body**

{     "UniqueID": "DQ4804-4804_00279465",     "Values": ["0.125","0.230","0.314","0.374","-0.412","0.428","0.424","0.403","-0.368","-0.323","0.270","0.213","-0.155","0.098","-0.046"],     "Channel": “0”,}

**Response → Status 200**

{

"ERROR_CODE": null,

"ERROR_DESCRIPTION": null

}

| **API** | **4.5.     SetOutputEqFIR** |
| --- | --- |
| **Type** | **POST** |
| **Description** | Through this command the client set the Output EQ FIR. |
| **Parameters** | **Identifier** |
| **1** | UniqueID |
| **2** | Values |
| **3** | Channel |
| **RESPONSE** |  |
| **Status Code** | 200 OK, 400 Bad Request, 401 Unauthorized |
| **Parameters** | **Identifier** |
|  | ERROR_CODE |
|  | ERROR_DESCRIPTION |

### 4.5.1. SetOutputEqFIR Example

**Endpoint**

POST /api/ARA/SetOutputEqFIR HTTP/1.1

**Header**

authClientToken: fcb0d2ee-9179-4968-8799-690fd242d530

**Body**

{     "UniqueID": "DQ4804-4804_00279465",     "Values": ["0.125","0.230","0.314","0.374","-0.412","0.428","0.424","0.403","-0.368","-0.323","0.270","0.213","-0.155","0.098","-0.046"],     "Channel": “0”,}

**Response → Status 200**

{

"ERROR_CODE": null,

"ERROR_DESCRIPTION": null

}

| **API** | **4.6.     SetOutputEqGain** |
| --- | --- |
| **Type** | **POST** |
| **Description** | Through this command the client set the Output EQ Gain. |
| **Parameters** | **Identifier** |
| **1** | UniqueID |
| **2** | Value |
| **3** | Channel |
| **RESPONSE** |  |
| **Status Code** | 200 OK, 400 Bad Request, 401 Unauthorized |
| **Parameters** | **Identifier** |
|  | ERROR_CODE |
|  | ERROR_DESCRIPTION |

### 4.6.1. SetOutputEqGain Example

**Endpoint**

POST /api/ARA/SetOutputEqGain HTTP/1.1

**Header**

authClientToken: fcb0d2ee-9179-4968-8799-690fd242d530

**Body**

{     "UniqueID": "DQ4804-4804_00279465",     "Value": “3.6”,     "Channel": “0”,}

**Response → Status 200**

{

"ERROR_CODE": null,

"ERROR_DESCRIPTION": null

}

| **API** | **4.7.     SetOutputEqPhase** |
| --- | --- |
| **Type** | **POST** |
| **Description** | Through this command the client set the Output EQ Phase. |
| **Parameters** | **Identifier** |
| **1** | UniqueID |
| **2** | Value |
| **3** | Channel |
| **RESPONSE** |  |
| **Status Code** | 200 OK, 400 Bad Request, 401 Unauthorized |
| **Parameters** | **Identifier** |
|  | ERROR_CODE |
|  | ERROR_DESCRIPTION |

### 4.7.1. SetOutputEqPhase Example

**Endpoint**

POST /api/ARA/SetOutputEqPhase HTTP/1.1

**Header**

authClientToken: fcb0d2ee-9179-4968-8799-690fd242d530

**Body**

{     "UniqueID": "DQ4804-4804_00279465",     "Value": true,     "Channel": “1”,}

**Response → Status 200**

{

"ERROR_CODE": null,

"ERROR_DESCRIPTION": null

}

| **API** | **4.8.     CreateAndAssignGroup** |
| --- | --- |
| **Type** | **POST** |
| **Description** | Through this command the client set up the Group configuration. |
| **Parameters** | **Identifier** |
| **1** | GroupLinks |
| **RESPONSE** |  |
| **Status Code** | 200 OK, 400 Bad Request, 401 Unauthorized |
| **Parameters** | **Identifier** |
| **1** | Guid |
| **2** | Successes |
| **3** | Errors |
|  | ERROR_CODE |
|  | ERROR_DESCRIPTION |

### 4.8.1. CreateAndAssignGroup Example

**Endpoint**

POST /api/ARA/CreateAndAssignGroup HTTP/1.1

**Header**

authClientToken: fcb0d2ee-9179-4968-8799-690fd242d530

**Body**

{     "GroupLinks": [           {

"UniqueID": "DQ4804-4804_0079465",                       "Channel": “0”

},           {

"UniqueID": "DQ4804-4804_0079465",                       "Channel": “2”

}     ]}

{

"GroupLinks": [

{

"UniqueID": "DQ4804-4804_0079465",

"Guid": "F1C074CC-9BAA-4AEE-B269-D38DBBE8CEB4",

"Channel": “0”,

}

]

}

**Response → Status 200**

{

"Guid": "F1C074CC-9BAA-4AEE-B269-D38DBBE8CEB4",

"Successes": {

"DQ4804-4804_0079465": {

"F1C074CC-9BAA-4AEE-B269-D38DBBE8CEB4": [ "0" , "2" ]

}

},

"Errors": {}

}

{

"Successes": {

"DQ4804-4804_0079465": {

"F1C074CC-9BAA-4AEE-B269-D38DBBE8CEB4": [ "0" ]

}

},

"Errors": {}

}

| **API** | **4.9.     UnassignGroup** |
| --- | --- |
| **Type** | **POST** |
| **Description** | Through this command the client set up the Group configuration. |
| **Parameters** | **Identifier** |
| **1** | GroupLinks |
| **RESPONSE** |  |
| **Status Code** | 200 OK, 400 Bad Request, 401 Unauthorized |
| **Parameters** | **Identifier** |
| **1** | Successes |
| **2** | Errors |
|  | ERROR_CODE |
|  | ERROR_DESCRIPTION |

### 4.9.1. UnassignGroup Example

**Endpoint**

POST /api/ARA/UnassignGroup HTTP/1.1

**Header**

authClientToken: fcb0d2ee-9179-4968-8799-690fd242d530

**Body**

{

"GroupLinks": [

{

"UniqueID": "DQ4804-4804_0079465",

"Guid": "F1C074CC-9BAA-4AEE-B269-D38DBBE8CEB4",

"Channel": “0”,

},

{

"UniqueID": "DQ4804-4804_0079465",

"Guid": "F1C074CC-9BAA-4AEE-B269-D38DBBE8CEB4",

"Channel": “1”,

}

]

}

**Response → Status 200**

{

"Successes": {

"DQ4804-4804_0079465": {

"F1C074CC-9BAA-4AEE-B269-D38DBBE8CEB4": [ "0", "1" ]

}

},

"Errors": {}

}

| **API** | **4.10.  OpenEntityDetails** |
| --- | --- |
| **Type** | **POST** |
| **Description** | Through this command the client can open and view the entity details. |
| **Parameters** | **Identifier** |
| **1** | UniqueID |
| **RESPONSE** |  |
| **Status Code** | 200 OK, 400 Bad Request, 401 Unauthorized |
| **Parameters** | **Identifier** |
|  | ERROR_CODE |
|  | ERROR_DESCRIPTION |

### 4.10.1. OpenEntityDetails Example

**Endpoint**

POST /api/ARA/OpenEntityDetails HTTP/1.1

**Header**

authClientToken: fcb0d2ee-9179-4968-8799-690fd242d530

**Body**

{     "UniqueID": "DQ4804-4804_0079465"}

**Response → Status 200**

{

"ERROR_CODE": null,    "ERROR_DESCRIPTION": null}