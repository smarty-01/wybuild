# ForgeAPK Production Starter

This is the deployable foundation: Next.js dashboard, GitHub OAuth, GitHub repo discovery, PostgreSQL/Prisma models, build API, isolated FastAPI worker, Docker Compose, APK/AAB Gradle path, quotas and artifact endpoint.

## Local
1. `cp .env.example .env.local`
2. `npm install`
3. `npm run db:generate`
4. `npm run db:push`
5. `docker compose up --build`
6. `npm run dev`

## GitHub
Create an OAuth App with callback `/api/auth/github/callback`, then set credentials in `.env.local`.

## Production
Use managed Postgres/Redis, a hardened disposable VM/container runtime, private object storage with expiring URLs, encrypted OAuth tokens, a secrets manager for signing keys, malware scanning, rate limits, billing, monitoring and HTTPS.

The worker intentionally requires a real Android SDK image. Install and pin command-line tools, platform SDK and build-tools in `worker/Dockerfile` before public deployment.

Never run untrusted source inside the web process or a privileged container.
