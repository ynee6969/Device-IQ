# Vercel Environment Fix

## What The Screenshot Means

The signup page is showing a service error because the app cannot complete account creation without a database connection.

## What To Fix In Vercel

1. Add `DATABASE_URL` to the Vercel project.
2. Point `DATABASE_URL` to the hosted PostgreSQL database used by Prisma.
3. Keep only one auth secret name active in deployment.
4. Prefer `AUTH_SECRET` and remove `NEXTAUTH_SECRET` if both are present.
5. Set `NEXTAUTH_URL` to the deployed site origin, not a local path.

## Recommended Auth Secret

Use a strong random secret for `AUTH_SECRET`.

Generate one with:

```bash
node -e "console.log(require('node:crypto').randomBytes(32).toString('base64url'))"
```

## Notes

- `DATABASE_URL` is required for signup, login, favorites, and other database-backed features.
- `AUTH_SECRET` is used to sign the auth session.
- `NEXTAUTH_SECRET` is only needed if you choose that secret name instead of `AUTH_SECRET`.
