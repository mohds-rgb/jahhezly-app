BLITZ DEPLOYMENT FIX

If blitz.cloud says requirements.txt is missing, make sure the repository root contains BOTH:
- requirements.txt
- Dockerfile

This requirements.txt points to the backend package in ./backend.
Do not put secrets in this file.
