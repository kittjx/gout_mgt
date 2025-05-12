# Records API Documentation

## Overview

The Records API allows users to create, retrieve, and delete health-related records. Each record has a specific type and associated data.

## Endpoints

### GET /records/

Retrieves all records for the authenticated user, grouped by record type.

**Response Example:**

```json
{
  "weight": [
    {
      "record_id": 1,
      "date": "2023-06-15T08:30:00Z",
      "value": "75.5"
    }
  ],
  "mainFood": [
    {
      "record_id": 2,
      "date": "2023-06-15T12:00:00Z",
      "name": "Rice",
      "amount": "200g"
    }
  ]
}
```

### POST /records/

Creates a new record.

**Request Body:**

```json
{
  "record_type": "weight",
  "date": "2023-06-15T08:30:00Z",
  "data": {
    "value": "75.5"
  }
}
```

**Response Example:**

```json
{
  "record_id": 1,
  "date": "2023-06-15T08:30:00Z",
  "value": "75.5"
}
```

### DELETE /records/{record_id}/

Deletes a record.

**Response:** HTTP 204 No Content

## Record Types

The following record types are supported:

1. **weight**
   - Required fields: `value` (decimal)

2. **mainFood**
   - Required fields: `name` (string), `amount` (string)

3. **waterIntake**
   - Required fields: `amount` (string)

4. **purineFood**
   - Required fields: `type` (string), `amount` (string)

5. **uricAcid**
   - Required fields: `value` (string)
   - Optional fields: `method` (string, default: "自测")

6. **urinePH**
   - Required fields: `value` (string)

7. **liverFunction**
   - Required fields: `value` (string)