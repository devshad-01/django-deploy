# Django Messaging App

A robust RESTful API for a messaging application built with Django and Django REST Framework.

## Features

- **User Management**: Custom user model with additional fields
- **Conversations**: Multi-participant conversations
- **Messages**: Real-time messaging within conversations
- **REST API**: Full CRUD operations for all resources
- **Admin Interface**: Django admin for easy management
- **Authentication**: Session-based authentication

## Project Structure

```
messaging_app/
├── manage.py
├── requirements.txt
├── messaging_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── chats/
    ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── migrations/
```

## Models

### User
Extended Django's AbstractUser with additional fields:
- `email` (unique)
- `first_name`, `last_name`
- `phone_number`
- `is_online`
- `created_at`, `updated_at`

### Conversation
Represents a conversation between multiple users:
- `participants` (many-to-many with User)
- `created_at`, `updated_at`

### Message
Individual messages within conversations:
- `sender` (foreign key to User)
- `conversation` (foreign key to Conversation)
- `content`
- `timestamp`
- `is_read`

## API Endpoints

### Base URL: `/api/`

### Users
- `GET /api/users/` - List all users
- `POST /api/users/` - Create a new user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Conversations
- `GET /api/conversations/` - List user's conversations
- `POST /api/conversations/` - Create a new conversation
- `GET /api/conversations/{id}/` - Get conversation details with messages
- `PUT /api/conversations/{id}/` - Update conversation
- `DELETE /api/conversations/{id}/` - Delete conversation
- `POST /api/conversations/{id}/add_participant/` - Add participant to conversation
- `POST /api/conversations/{id}/remove_participant/` - Remove participant from conversation

### Messages
- `GET /api/messages/` - List messages (filterable by conversation_id)
- `POST /api/messages/` - Send a new message
- `GET /api/messages/{id}/` - Get message details
- `PUT /api/messages/{id}/` - Update message
- `DELETE /api/messages/{id}/` - Delete message
- `PATCH /api/messages/{id}/mark_as_read/` - Mark message as read
- `POST /api/messages/mark_conversation_as_read/` - Mark all messages in conversation as read

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd messaging_app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

## Usage Examples

### Create a Conversation
```bash
curl -X POST http://localhost:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{"participant_ids": [2, 3]}'
```

### Send a Message
```bash
curl -X POST http://localhost:8000/api/messages/ \
  -H "Content-Type: application/json" \
  -d '{
    "conversation": 1,
    "content": "Hello, world!"
  }'
```

### Get Conversations
```bash
curl -X GET http://localhost:8000/api/conversations/
```

## Authentication

The API uses Django's session authentication. Users need to authenticate through:
- Django admin interface (`/admin/`)
- Custom authentication endpoints (can be added)

## Admin Interface

Access the admin interface at `/admin/` to:
- Manage users, conversations, and messages
- View conversation participants
- Monitor message activity

## Development Features

- **Pagination**: Automatic pagination for list endpoints
- **Filtering**: Search users and filter messages by conversation
- **Validation**: Comprehensive input validation
- **Error Handling**: Proper HTTP status codes and error messages
- **Performance**: Optimized queries with select_related and prefetch_related

## Security Considerations

- Authentication required for all endpoints
- Users can only access conversations they participate in
- Input validation and sanitization
- CSRF protection enabled

## Testing

Run tests with:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
