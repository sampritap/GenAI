# JWT Authentication Learning Tasks

Learn JWT authentication in FastAPI with practical examples.

## Task 1: JWT Basics

Covers fundamental JWT authentication concepts:
- Password hashing with bcrypt
- Creating JWT tokens
- Token verification
- Protected endpoints with `Depends()`

**Run:**
```bash
uvicorn learning_tasks.auth.task_1_jwt_basics:app --reload
```

**Test Credentials:**
- Username: `john`
- Password: `secret`

**Test Flow:**
```bash
# 1. Login
curl -X POST "http://localhost:8000/login?username=john&password=secret"

# 2. Use token
curl -H "Authorization: Bearer <token>" http://localhost:8000/me
```

## Task 2: JWT Advanced

Covers advanced authentication patterns:
- Refresh tokens (long-lived)
- Access tokens (short-lived)
- Role-based access control (RBAC)
- Admin-only endpoints
- Token blacklist/logout

**Run:**
```bash
uvicorn learning_tasks.auth.task_2_jwt_advanced:app --reload
```

**Test Credentials:**
- Admin: `admin` / `secret` (ADMIN role)
- User: `john` / `secret` (USER role)
- Guest: `guest` / `secret` (GUEST role)

**Test Flow:**
```bash
# 1. Login as admin
curl -X POST "http://localhost:8000/login?username=admin&password=secret"

# 2. Use access token
curl -H "Authorization: Bearer <access_token>" http://localhost:8000/admin-only

# 3. Refresh token
curl -X POST "http://localhost:8000/refresh" \
     -H "Content-Type: application/json" \
     -d '{"refresh_token": "<refresh_token>"}'
```

## Key Concepts

| Concept | What | When |
|---------|------|------|
| **Access Token** | Short-lived (15 min) | Every request |
| **Refresh Token** | Long-lived (7 days) | Get new access token |
| **JWT Payload** | `{"sub": "user", "exp": 1234567}` | Contains user info |
| **Password Hash** | `$2b$12$...` (bcrypt) | Store securely |
| **Bearer Token** | `Authorization: Bearer <token>` | HTTP header |
| **Role-Based** | ADMIN, USER, GUEST | Access control |

## Best Practices

✓ **DO:**
- Use HTTPS in production
- Store SECRET_KEY as environment variable
- Use strong, unique secret keys (32+ characters)
- Set short expiration times (15-30 min)
- Hash passwords with bcrypt/argon2
- Validate token signature and expiration
- Use refresh tokens for long-term access

✗ **DON'T:**
- Expose SECRET_KEY in code
- Store plain-text passwords
- Use weak secret keys
- Log sensitive data
- Trust client-provided user ID
- Use same key for access and refresh tokens

## Production Considerations

1. **Store tokens:** Use secure, httponly cookies
2. **Revocation:** Use Redis for token blacklist
3. **Rate limiting:** Limit login attempts
4. **Audit logging:** Log authentication events
5. **Database:** Replace fake_users_db with real database
6. **Email verification:** Verify emails before login
7. **HTTPS only:** Use HTTPS/TLS in production

## Further Learning

- [ ] Add email verification
- [ ] Add password reset flow
- [ ] Add OAuth2 (Google, GitHub login)
- [ ] Add multi-factor authentication (MFA)
- [ ] Add social login
- [ ] Implement token refresh automatically in frontend
- [ ] Add CORS for frontend integration
