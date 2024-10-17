# todo

1. Modularize;
2. Connect frontend endpoints to DB;
3. Add login/register opt;
4. Document;
5. Implement Auth and verification.
6. Fix layouts (layout -> task page layout -> edit layout (?))

### Data for Postman

`User`

```json
[
    {
        "email": "another@mail.com",
        "id": 1,
        "name": "Antanas",
        "password": "ilhwDCLNWOWŪŲCYWDNĘČX.C.SANHXIUSACXHD"
    },
    {
        "email": "just@mail.com",
        "id": 2,
        "name": "Ona",
        "password": "ilhwDCLNWOWŪŲCYWDNĘČX.C.SANHXIUSACXHD"
    }
]
```

`Task`

```json
[
    {
        "completed": true,
        "content": "Any string content jsonified",
        "created": "2024-10-05T19:53:52.709441",
        "id": 1,
        "user_id": 1
    },
    {
        "completed": true,
        "content": "Another task",
        "created": "2024-10-05T19:56:41.963936",
        "id": 2,
        "user_id": 1
    }
],
[
    {
        "completed": false,
        "content": "This one also has",
        "created": "2024-10-05T19:57:08.065741",
        "id": 3,
        "user_id": 2
    }
]
```
