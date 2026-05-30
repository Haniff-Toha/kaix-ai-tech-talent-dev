# Knowledge RAG — Content Structure Template
### Kaix · Career Knowledge Base
**Reference track:** Backend Engineer  
**Version:** 1.0  
**Format:** Each `---chunk---` block = one embedded document stored as a single row in `knowledge_rag`

> **How to use this template:**  
> Each chunk has a metadata header (`###`) followed by the content body. The metadata maps directly to the `knowledge_rag` table columns. Replicate this structure for all 8 career tracks. The Backend Engineer track below is the full reference — use it as the pattern.

---

## Chunk Metadata Schema

Every chunk stored in `knowledge_rag` carries this metadata in the `metadata JSONB` column:

```json
{
  "career_track": "backend_engineer",
  "content_type": "role_definition | skill_taxonomy | skill_description | milestone_template | resource | blocker_pattern | career_transition | salary_context",
  "skill_name": "string or null",
  "seniority": "all | beginner | junior | mid | senior | lead",
  "language": "en | id",
  "translation_pair_id": "uuid (links EN and ID versions of the same chunk)",
  "tags": ["array", "of", "topic", "tags"]
}
```

> Store EN and ID versions as **separate rows** linked by `translation_pair_id`.  
> Never mix languages in one chunk — it degrades embedding quality.  
> At query time: filter by `metadata->>'language' = user.preferred_language` before semantic search.

---

---

# TRACK: Backend Engineer

---

## 1. Role Definition

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "role_definition",
  "skill_name": null,
  "seniority": "all",
  "language": "en",
  "tags": ["role", "overview", "backend", "what-is"]
}
```
### Content
A Backend Engineer designs, builds, and maintains the server-side systems that power applications. They are responsible for the logic, databases, APIs, and infrastructure that users never see but depend on entirely. Unlike frontend engineers who build what users interact with, backend engineers build what makes those interactions work — data storage, business logic, authentication, integrations, and performance at scale.

Day-to-day work involves writing server-side code, designing database schemas, building and maintaining REST or GraphQL APIs, handling authentication and authorization, optimizing slow queries, debugging production incidents, and collaborating with frontend engineers on API contracts.

Backend engineers work in languages such as Python, Go, Node.js, Java, Ruby, or Rust. The choice of language depends on the company, the team, and the problem domain — but the underlying concepts (data modeling, API design, concurrency, system design) transfer across all of them.

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "role_definition",
  "skill_name": null,
  "seniority": "all",
  "language": "id",
  "tags": ["role", "overview", "backend", "what-is"]
}
```
### Content
Backend Engineer adalah profesional yang merancang, membangun, dan memelihara sistem server-side yang menggerakkan aplikasi. Mereka bertanggung jawab atas logika bisnis, database, API, dan infrastruktur yang tidak terlihat oleh pengguna namun menjadi fondasi dari semua yang berjalan.

Pekerjaan sehari-hari meliputi: menulis kode server-side, merancang skema database, membangun dan memelihara REST atau GraphQL API, menangani autentikasi dan otorisasi, mengoptimasi query yang lambat, debugging insiden produksi, dan berkolaborasi dengan frontend engineer terkait kontrak API.

Backend engineer bekerja dengan bahasa seperti Python, Go, Node.js, Java, Ruby, atau Rust. Pilihan bahasa bergantung pada perusahaan dan domain masalah — namun konsep dasarnya (pemodelan data, desain API, konkurensi, desain sistem) berlaku di semua bahasa.

---

## 2. Seniority Levels

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "role_definition",
  "skill_name": null,
  "seniority": "all",
  "language": "en",
  "tags": ["seniority", "levels", "career-ladder", "junior", "mid", "senior"]
}
```
### Content
**Junior Backend Engineer (0–2 years)**
Writes code under supervision. Implements well-defined features. Understands basic CRUD operations, REST APIs, and relational databases. Requires frequent code review. Focuses on learning one language deeply. Typical tasks: building API endpoints from specs, writing unit tests, fixing bugs, consuming third-party APIs.

**Mid-level Backend Engineer (2–5 years)**
Works independently on features. Designs database schemas. Writes production-ready code with minimal review. Understands performance tradeoffs. Can debug complex issues. Begins contributing to system design discussions. Typical tasks: designing new service modules, database optimization, building internal tools, mentoring juniors informally.

**Senior Backend Engineer (5–8 years)**
Leads technical design for significant features or services. Defines API contracts. Identifies architectural risks. Reviews code for the whole team. Contributes to engineering standards. Mentors mid-level engineers. Typical tasks: system design documents, architecture decisions, cross-team API design, performance audits, technical interviews.

**Lead / Staff Backend Engineer (8+ years)**
Sets the technical direction for a domain or entire backend. Coordinates across multiple teams. Defines standards and patterns used org-wide. Builds alignment between engineering and product. Typical tasks: long-term architecture planning, engineering roadmap, cross-functional technical leadership.

---

## 3. Skill Taxonomy (Ordered Dependency Tree)

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "skill_taxonomy",
  "skill_name": null,
  "seniority": "beginner",
  "language": "en",
  "tags": ["skill-order", "learning-sequence", "foundations", "beginner"]
}
```
### Content
**Phase 1 — Foundations (must be learned in this order)**

The following skills have hard dependencies. Do not skip ahead. Each skill listed below requires the one before it.

1. **Programming fundamentals** — Variables, data types, conditionals, loops, functions. Must be solid before anything else. Language recommendation for beginners: Python.
2. **Object-oriented programming (OOP)** — Classes, inheritance, encapsulation, polymorphism. Required before building any non-trivial system.
3. **Data structures & algorithms basics** — Arrays, linked lists, hashmaps, stacks, queues, basic sorting. Required for writing efficient code and passing technical interviews.
4. **Git & version control** — Commits, branches, merges, pull requests. Required to collaborate on any real codebase.
5. **Command line / Linux basics** — File navigation, permissions, processes, environment variables. Required to work on any server or cloud environment.
6. **HTTP & the web** — Request/response cycle, status codes, headers, methods (GET, POST, PUT, DELETE). Required before building any API.
7. **Relational databases & SQL** — Tables, primary keys, foreign keys, SELECT, INSERT, UPDATE, DELETE, JOINs, indexes. Required before any backend work.
8. **Building a REST API** — Routes, controllers, middleware, request validation, error handling. First major integration of all foundational skills.

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "skill_taxonomy",
  "skill_name": null,
  "seniority": "junior",
  "language": "en",
  "tags": ["skill-order", "learning-sequence", "junior", "intermediate"]
}
```
### Content
**Phase 2 — Junior to Mid (requires Phase 1 complete)**

1. **Authentication & authorization** — Sessions, JWT, OAuth2, bcrypt password hashing, role-based access control. Required for any real app.
2. **Database design** — Normalization (1NF–3NF), ER diagrams, schema migrations, indexing strategy. Required before building production systems.
3. **ORM usage** — SQLAlchemy (Python), Prisma (Node), Hibernate (Java). Understand what the ORM generates in SQL.
4. **API design principles** — RESTful conventions, versioning, pagination, rate limiting, consistent error formats.
5. **Testing** — Unit tests, integration tests, mocking, test coverage. Required for production code.
6. **Environment management** — .env files, secrets management, dev/staging/production parity.
7. **NoSQL databases** — MongoDB or Redis. Understand when to use instead of SQL — not as a replacement but as a complement.
8. **Asynchronous programming** — Async/await, event loops, background tasks. Required for any I/O-heavy application.
9. **Containerization basics** — Docker, Dockerfile, docker-compose. Required for modern deployment workflows.

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "skill_taxonomy",
  "skill_name": null,
  "seniority": "mid",
  "language": "en",
  "tags": ["skill-order", "learning-sequence", "mid", "senior", "advanced"]
}
```
### Content
**Phase 3 — Mid to Senior (requires Phase 2 complete)**

1. **System design fundamentals** — Load balancing, caching strategies (Redis, CDN), database read replicas, horizontal vs vertical scaling. The most important skill jump between mid and senior.
2. **Message queues & async architecture** — RabbitMQ, Kafka, Celery. Required for decoupled, scalable systems.
3. **API security** — OWASP Top 10, SQL injection prevention, XSS, CSRF, rate limiting, input sanitization.
4. **Performance & query optimization** — EXPLAIN ANALYZE, N+1 problem, query caching, connection pooling.
5. **Cloud fundamentals** — AWS or GCP basics: EC2/Compute Engine, S3/Cloud Storage, RDS, IAM, VPC. Not deep expertise — enough to deploy and reason about infrastructure.
6. **CI/CD pipelines** — GitHub Actions or GitLab CI: automated testing, linting, deployment pipelines.
7. **Observability** — Logging (structured JSON), metrics (Prometheus/Grafana), tracing (OpenTelemetry), alerting.
8. **Microservices basics** — When to break a monolith, service boundaries, inter-service communication (REST vs gRPC vs events).
9. **WebSockets & real-time** — Long polling vs SSE vs WebSockets. Required for chat, notifications, live data features.

---

## 4. Skill Descriptions

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "skill_description",
  "skill_name": "REST API design",
  "seniority": "junior",
  "language": "en",
  "tags": ["api", "rest", "http", "design"]
}
```
### Content
**REST API design** (desain REST API) is the practice of building HTTP APIs that follow consistent, predictable conventions. A well-designed REST API is easy for frontend engineers and third-party developers to use without reading extensive documentation.

Key principles: use nouns not verbs in URLs (`/users/123` not `/getUser`), use HTTP methods semantically (GET to read, POST to create, PUT/PATCH to update, DELETE to remove), return consistent response shapes, use appropriate status codes (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Internal Server Error), support pagination on list endpoints, version your API (`/v1/users`).

Common beginner mistakes: using GET for state-changing operations, inconsistent error formats, returning 200 for errors, not validating request input, exposing internal database IDs without consideration.

At junior level: implement endpoints from a given spec correctly. At mid level: design the API contract itself, including edge cases and error handling. At senior level: define API standards for the team, review API designs across services.

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "skill_description",
  "skill_name": "database design",
  "seniority": "junior",
  "language": "en",
  "tags": ["database", "sql", "schema", "normalization", "postgres"]
}
```
### Content
**Database design** is the process of structuring data in a relational database so it is accurate, consistent, and efficient to query. Poor database design is one of the most common sources of long-term technical debt in backend systems.

Core concepts: normalization (organizing data to reduce redundancy — 1NF removes repeating groups, 2NF removes partial dependencies, 3NF removes transitive dependencies), primary keys (unique identifier for each row), foreign keys (references to other tables, enforces referential integrity), indexes (speed up reads at the cost of write performance and storage), constraints (NOT NULL, UNIQUE, CHECK — enforce data integrity at the database level).

When to denormalize: when read performance is critical and data changes infrequently. Denormalization trades write complexity for read speed — valid in analytics/reporting contexts.

Common beginner mistakes: storing arrays or JSON where relational rows should be used, no indexes on foreign key columns, using VARCHAR for everything, no consideration of cascading deletes, ignoring NULL semantics.

Recommended practice: design the schema on paper (or in dbdiagram.io) before writing a single line of code. Think about which queries will run most frequently and design indexes to support them.

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "skill_description",
  "skill_name": "sistem desain",
  "seniority": "mid",
  "language": "id",
  "tags": ["system-design", "scalability", "architecture", "caching", "load-balancer"]
}
```
### Content
**Sistem desain** (system design) adalah kemampuan merancang arsitektur sistem yang dapat menangani beban besar, tetap tersedia (highly available), dan mudah dipelihara seiring waktu. Ini adalah skill yang paling membedakan engineer mid-level dari senior.

Konsep inti yang harus dikuasai:

**Load balancing** — mendistribusikan traffic ke beberapa server agar tidak ada satu titik kegagalan. Tools: Nginx, AWS ALB.

**Caching** — menyimpan hasil komputasi atau query yang mahal agar tidak perlu diulang. Redis adalah pilihan utama. Strategi: cache-aside, write-through, TTL-based expiry.

**Database scaling** — read replicas untuk membagi beban baca; sharding untuk membagi data secara horizontal; connection pooling (PgBouncer) untuk mengelola koneksi database.

**Asynchronous processing** — operasi berat (email, laporan, AI calls) tidak boleh dijalankan secara sinkron di request handler. Gunakan task queue seperti Celery + Redis.

**CAP theorem** — sistem terdistribusi tidak bisa sekaligus konsisten, tersedia, dan toleran terhadap partisi jaringan. Harus memilih tradeoff yang sesuai dengan kebutuhan bisnis.

Cara belajar terbaik: kerjakan latihan sistem desain dari "System Design Primer" (GitHub) dan buku "Designing Data-Intensive Applications" oleh Martin Kleppmann.

---

## 5. Milestone Templates

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "milestone_template",
  "skill_name": null,
  "seniority": "beginner",
  "language": "en",
  "tags": ["milestone", "phase-1", "foundations", "template"]
}
```
### Content
**Milestone template: Backend Foundations (Phase 1)**
Target seniority jump: Complete beginner → Junior-ready  
Typical duration: 8–12 weeks at 1hr/day

Milestone 1.1 — Programming fundamentals solid
- Complete a structured Python course (not just tutorials — a full course with exercises)
- Build 3 small CLI programs from scratch (calculator, todo list, file organizer)
- Understand and explain: variables, loops, functions, error handling, file I/O
- Signal of completion: can build a small Python program without looking anything up

Milestone 1.2 — Databases and SQL comfortable
- Complete a SQL course covering SELECT, JOINs, subqueries, indexes
- Design a database schema for a simple app (e.g. a blog: users, posts, comments, tags)
- Write 20 progressively harder SQL queries on a real dataset
- Signal of completion: can write a multi-table JOIN query with filtering and ordering confidently

Milestone 1.3 — First REST API built and deployed
- Build a REST API with at least 5 endpoints (CRUD for one resource)
- Connect it to a real Postgres database
- Add basic authentication (JWT)
- Deploy it to a free platform (Railway, Render, or Fly.io)
- Write at least 10 unit tests
- Signal of completion: the API is live, someone else can use it, it has a README

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "milestone_template",
  "skill_name": null,
  "seniority": "junior",
  "language": "en",
  "tags": ["milestone", "phase-2", "junior-to-mid", "template"]
}
```
### Content
**Milestone template: Junior to Mid-level (Phase 2)**
Target seniority jump: Junior → Mid-level  
Typical duration: 12–18 months of professional work or 6–8 months of intensive self-study

Milestone 2.1 — Production-grade API architecture
- Refactor a project to use proper layered architecture (router → service → repository)
- Implement pagination, filtering, and sorting on list endpoints
- Add structured error handling with consistent error response format
- Write integration tests that test the full request/response cycle
- Signal of completion: a senior engineer reviews the code and has no major structural feedback

Milestone 2.2 — Database design ownership
- Design the full database schema for a non-trivial app (5+ tables with relationships)
- Write and run migrations using Alembic or a similar tool
- Identify and fix at least one N+1 query problem using EXPLAIN ANALYZE
- Implement soft deletes, audit timestamps (created_at, updated_at)
- Signal of completion: can explain every design decision in the schema confidently

Milestone 2.3 — Asynchronous system in production
- Integrate a task queue (Celery + Redis or similar)
- Move at least one slow operation (email, report generation, AI call) to async processing
- Handle task failures with retries and dead-letter queues
- Signal of completion: no user-facing endpoint takes more than 300ms due to heavy operations

Milestone 2.4 — Containerized deployment
- Write a production-ready Dockerfile for the API
- Set up docker-compose for local development with DB + Redis
- Deploy via CI/CD pipeline (GitHub Actions) with automated tests before deploy
- Signal of completion: `git push` triggers tests and deploys automatically

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "milestone_template",
  "skill_name": null,
  "seniority": "mid",
  "language": "en",
  "tags": ["milestone", "phase-3", "mid-to-senior", "template"]
}
```
### Content
**Milestone template: Mid to Senior (Phase 3)**
Target seniority jump: Mid → Senior  
Typical duration: 2–4 years of professional experience or 12–18 months intensive study + projects

Milestone 3.1 — System design capability demonstrated
- Complete 20 system design practice problems (from System Design Primer)
- Design 3 real systems end-to-end on paper: include DB schema, API design, caching strategy, scaling considerations
- Read and summarize 5 chapters of "Designing Data-Intensive Applications"
- Signal of completion: can whiteboard a system design for a simple app (URL shortener, ride-sharing, notification service) without prompting

Milestone 3.2 — Performance ownership
- Profile a slow API endpoint and reduce response time by > 50%
- Implement Redis caching with proper TTL and invalidation strategy
- Set up connection pooling (PgBouncer) for a high-traffic endpoint
- Write a load test and interpret the results
- Signal of completion: can diagnose a slow endpoint using only logs and query analysis tools

Milestone 3.3 — Observability and production readiness
- Implement structured JSON logging across an entire service
- Set up Prometheus metrics + Grafana dashboard for a service
- Define SLIs and SLOs for a critical endpoint
- Create a runbook for the top 3 most likely production incidents
- Signal of completion: if the service goes down at 2am, there is enough observability to diagnose and fix it within 30 minutes

---

## 6. Learning Resources

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "resource",
  "skill_name": "python",
  "seniority": "beginner",
  "language": "en",
  "tags": ["resource", "python", "beginner", "book", "course"]
}
```
### Content
**Resources for learning Python (beginner level)**

Books:
- "Automate the Boring Stuff with Python" by Al Sweigart — free online at automatetheboringstuff.com. Best for complete beginners. Practical, project-based.
- "Python Crash Course" by Eric Matthes — more structured than Automate. Good for people who prefer a textbook format.

Courses:
- CS50P (Harvard, free on edX) — rigorous, teaches Python with strong fundamentals. Recommended over quick YouTube tutorials.
- Dicoding "Belajar Dasar Pemrograman Python" — Bahasa Indonesia, structured, has assessments. Good for Indonesian learners who prefer to learn in their first language.

Practice platforms:
- Exercism.io (Python track) — structured exercises with mentor feedback. Better than LeetCode for fundamentals.
- HackerRank Python track — good for building speed and confidence on basic problems.

Avoid: random YouTube tutorial playlists without a structured exercise component. Watching code being written is not the same as writing code.

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "resource",
  "skill_name": "sistem desain",
  "seniority": "mid",
  "language": "id",
  "tags": ["resource", "system-design", "mid", "senior", "book", "github"]
}
```
### Content
**Sumber belajar sistem desain (level mid-senior)**

Buku:
- "Designing Data-Intensive Applications" oleh Martin Kleppmann — wajib dibaca oleh setiap backend engineer yang ingin mencapai level senior. Membahas database internal, replikasi, konsistensi, dan streaming data secara mendalam.
- "System Design Interview" oleh Alex Xu — lebih ringan dari Kleppmann, fokus pada pola-pola yang sering muncul dalam wawancara sistem desain.

GitHub:
- System Design Primer (github.com/donnemartin/system-design-primer) — gratis, lengkap, berisi latihan soal dengan jawaban. Titik awal terbaik untuk belajar sistem desain secara mandiri.

YouTube:
- ByteByteGo channel — visualisasi konsep sistem desain yang mudah dipahami. Cocok untuk membangun intuisi sebelum membaca buku yang lebih dalam.

Cara belajar yang efektif: jangan hanya membaca — setelah setiap konsep, coba gambar arsitekturnya sendiri di kertas tanpa melihat referensi. Kemudian bandingkan dengan solusi yang ada.

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "resource",
  "skill_name": "SQL and databases",
  "seniority": "beginner",
  "language": "en",
  "tags": ["resource", "sql", "postgres", "database", "beginner"]
}
```
### Content
**Resources for learning SQL and databases (beginner to junior)**

Interactive learning:
- SQLZoo (sqlzoo.net) — browser-based SQL practice, no setup required. Best first resource.
- Mode Analytics SQL Tutorial — free, progressive difficulty, uses real datasets.
- pgexercises.com — PostgreSQL-specific exercises. Highly recommended since Postgres is the industry standard.

Courses:
- CS50 SQL (Harvard, free) — rigorous introduction to databases. Covers SQL, schema design, and indexes.
- Dicoding "Belajar Fundamental Aplikasi Back-End" — covers Node.js with database integration in Bahasa Indonesia.

Tools to set up locally:
- PostgreSQL + pgAdmin or TablePlus for a GUI. Installing Postgres locally is a required skill — don't rely only on online sandboxes.

Books (when ready to go deeper):
- "Learning SQL" by Alan Beaulieu — comprehensive SQL reference, good for mid-level.
- PostgreSQL official documentation — surprisingly readable, use it as a reference not a tutorial.

---

## 7. Blocker Patterns & Recovery

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "blocker_pattern",
  "skill_name": "async programming",
  "seniority": "junior",
  "language": "en",
  "tags": ["blocker", "async", "concurrency", "mental-model", "recovery"]
}
```
### Content
**Common blocker: Async programming mental model**

Symptom: The user understands synchronous code well but gets confused when async/await is introduced. They understand the syntax but don't understand *why* code runs in a particular order. Common confusion points: why `await` is needed, what an event loop is, why you can't just call an async function like a regular one.

Root cause: Async programming requires a fundamentally different mental model of how code executes. Most beginners learn synchronous execution (line by line, top to bottom) and then try to apply that model to async code — which doesn't work.

Recovery approach:
1. Stop writing async code for 2 days. Spend those days building a solid mental model first.
2. Watch a visual explanation of the JavaScript event loop (even if you're learning Python — the concept is identical). The video "What the heck is the event loop anyway?" by Philip Roberts (JSConf 2014) is the clearest explanation that exists.
3. Then return to Python: understand that `asyncio` is Python's event loop. `await` means "pause here and let other tasks run while I wait."
4. Write a small program that makes 5 HTTP requests — first synchronously (one by one), then asynchronously (all at once with asyncio.gather). Measure the time difference. This makes the value of async concrete.

Signal of recovery: Can explain what happens step-by-step when `await asyncio.gather(task1, task2, task3)` is called.

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "blocker_pattern",
  "skill_name": "database design",
  "seniority": "junior",
  "language": "en",
  "tags": ["blocker", "database", "schema", "normalization", "recovery"]
}
```
### Content
**Common blocker: Schema design paralysis**

Symptom: User understands SQL queries but freezes when asked to design a database schema from scratch. They don't know where to start, how many tables to create, what belongs in its own table vs as a column, or how to handle many-to-many relationships.

Root cause: Schema design is not taught well in most courses, which focus on querying existing schemas rather than creating them. It requires pattern recognition that comes from seeing many examples.

Recovery approach:
1. Study 5 real schema designs before designing your own. Look at: a blog (users, posts, comments, tags), an e-commerce store (products, orders, order_items, users, addresses), a social network (users, follows, posts, likes), a booking system (users, resources, reservations, time_slots), a SaaS app (users, organizations, memberships, subscriptions).
2. For each example, draw the ER diagram yourself after reading the description — before looking at the actual schema. Then compare.
3. Internalize the two key rules: (a) if data repeats in multiple rows, it belongs in its own table; (b) many-to-many relationships always need a junction table.
4. Design your own schema for a simple app you use (e.g. a recipe app, a habit tracker). Get it reviewed.

Signal of recovery: Can design a 5-table schema for a described app in under 30 minutes with proper foreign keys and at least one many-to-many relationship handled correctly.

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "blocker_pattern",
  "skill_name": "motivasi dan konsistensi",
  "seniority": "all",
  "language": "id",
  "tags": ["blocker", "motivation", "procrastination", "consistency", "recovery"]
}
```
### Content
**Blocker umum: Kehilangan motivasi di tengah jalan**

Gejala: Pengguna semangat di awal belajar backend, menyelesaikan beberapa tutorial, lalu tiba-tiba berhenti selama 2–3 minggu. Ketika kembali, merasa harus mulai dari awal lagi. Siklus ini berulang.

Penyebab: Tutorial memberikan dopamin instan karena hasilnya terlihat langsung. Ketika mulai membangun sesuatu sendiri, tidak ada panduan langkah demi langkah — dan ketidakpastian ini memicu avoidance.

Strategi pemulihan:
1. Berhenti menonton tutorial. Mulai bangun sesuatu — meskipun kecil dan jelek. Sebuah API dengan 3 endpoint yang kamu buat sendiri mengajarkan lebih banyak dari 10 tutorial yang kamu tonton.
2. Gunakan "minimum viable session" — komitmen hanya 15 menit per hari di hari-hari sulit. Membuka editor dan menulis satu fungsi sudah cukup untuk mempertahankan momentum.
3. Buat progres terlihat. Gunakan GitHub dengan commit harian — melihat contribution graph yang terisi membantu otak merasakan kemajuan.
4. Temukan komunitas. Bergabung dengan Discord backend Indonesia atau forum Dicoding. Belajar bersama orang lain secara signifikan mengurangi dropout rate.

Tanda pemulihan: Kembali ke sesi belajar secara konsisten selama 5 hari berturut-turut tanpa merasa perlu "mengulang dari awal."

---

## 8. Salary Context (Indonesian/SEA Market)

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "salary_context",
  "skill_name": null,
  "seniority": "all",
  "language": "en",
  "tags": ["salary", "indonesia", "sea", "market", "compensation"]
}
```
### Content
**Backend Engineer compensation — Indonesian & SEA market (2026 estimates)**

Figures are approximate monthly gross salary in Indonesian Rupiah (IDR) for full-time employed positions in Jakarta and major tech hubs. Remote international roles typically pay significantly more.

| Level | Jakarta (IDR/month) | SEA Remote (USD/month) |
|---|---|---|
| Junior (0–2yr) | Rp 6–12 juta | $800–1,500 |
| Mid-level (2–5yr) | Rp 12–25 juta | $1,500–3,500 |
| Senior (5–8yr) | Rp 25–50 juta | $3,500–7,000 |
| Lead/Staff (8yr+) | Rp 50–100 juta | $7,000–15,000+ |

Key skills that command premium compensation at each level:
- Junior premium: Python + FastAPI or Node.js + TypeScript over PHP-only
- Mid premium: System design knowledge, cloud (AWS/GCP), Golang
- Senior premium: Distributed systems, Kafka, deep Postgres optimization
- Lead premium: Engineering leadership experience, cross-functional influence

Remote international opportunities (via Toptal, Arc.dev, or direct outreach) typically pay 3–5x local Jakarta rates for the same skill level. Reaching mid-level with strong English communication opens access to this market.

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "salary_context",
  "skill_name": null,
  "seniority": "all",
  "language": "id",
  "tags": ["salary", "indonesia", "sea", "market", "compensation"]
}
```
### Content
**Kompensasi Backend Engineer — Pasar Indonesia & SEA (estimasi 2026)**

Angka di bawah adalah perkiraan gaji bulanan bruto dalam Rupiah untuk posisi full-time di Jakarta dan kota teknologi utama lainnya. Posisi remote internasional umumnya membayar jauh lebih tinggi.

| Level | Jakarta (IDR/bulan) | Remote SEA (USD/bulan) |
|---|---|---|
| Junior (0–2thn) | Rp 6–12 juta | $800–1.500 |
| Mid-level (2–5thn) | Rp 12–25 juta | $1.500–3.500 |
| Senior (5–8thn) | Rp 25–50 juta | $3.500–7.000 |
| Lead/Staff (8thn+) | Rp 50–100 juta | $7.000–15.000+ |

Skill yang meningkatkan nilai kompensasi secara signifikan:
- Level junior: Python + FastAPI atau Node.js + TypeScript lebih bernilai dari PHP saja
- Level mid: pengetahuan sistem desain, cloud (AWS/GCP), Golang
- Level senior: distributed systems, Kafka, optimasi Postgres tingkat lanjut
- Level lead: pengalaman kepemimpinan teknis, kemampuan komunikasi lintas tim

Peluang remote internasional (melalui Toptal, Arc.dev, atau outreach langsung) umumnya membayar 3–5x lipat gaji Jakarta untuk level yang sama. Mencapai level mid dengan kemampuan komunikasi Bahasa Inggris yang kuat membuka akses ke pasar ini.

---

## 9. Career Transition Patterns

---chunk---
### Metadata
```json
{
  "career_track": "backend_engineer",
  "content_type": "career_transition",
  "skill_name": null,
  "seniority": "all",
  "language": "en",
  "tags": ["transition", "career-change", "from", "pivot"]
}
```
### Content
**Common career paths into Backend Engineering**

**From Frontend Engineer:**
Easiest transition. Already knows HTTP, APIs, and Git. Needs to learn: server-side language deeply, database design, auth patterns, deployment. Typical transition time: 3–6 months of focused effort. Advantage: understands the full stack, which makes for better API design.

**From Data Analyst / Data Science:**
Already knows Python and SQL well — two of the most important backend skills. Needs to learn: API design, web frameworks (FastAPI recommended given Python familiarity), authentication, deployment, async programming. Typical transition time: 4–8 months. Advantage: strong database intuition from the start.

**From IT Support / System Administrator:**
Already understands Linux, networking, and servers — valuable for DevOps-adjacent backend work. Needs to learn: programming fundamentals first, then web frameworks, then databases. Steeper learning curve on the programming side. Typical transition time: 8–14 months.

**From Complete Beginner (no tech background):**
Longest path but fully achievable. Recommended sequence: Python fundamentals (2–3 months) → databases (1–2 months) → first API (1–2 months) → junior-ready portfolio (2–3 months). Total: 6–10 months of 1–2hr/day consistent practice. The biggest risk is tutorial hell — commit to building projects early.

**From Backend to adjacent roles:**
- Backend → DevOps/SRE: add infrastructure, CI/CD, and observability skills (6–12 months)
- Backend → ML Engineer: add Python ML libraries, model training, MLOps (8–14 months)
- Backend → Engineering Lead: develop people management, system design mastery, and communication skills (2–4 years of senior IC experience first)

---

---

# HOW TO REPLICATE FOR OTHER TRACKS

Use the Backend Engineer track above as the exact template. For each of the remaining 7 tracks, create the same 9 section types:

1. Role Definition (EN + ID)
2. Seniority Levels (EN + ID)
3. Skill Taxonomy — Phase 1 / Phase 2 / Phase 3 (EN + ID per phase)
4. Skill Descriptions — 4–6 key skills per track (EN + ID)
5. Milestone Templates — one per phase (EN + ID)
6. Learning Resources — 2–3 resource chunks per track (EN + ID)
7. Blocker Patterns — 2–3 common blockers per track (EN + ID)
8. Salary Context (EN + ID)
9. Career Transition Patterns (EN + ID)

**Minimum chunk count per track:** ~40–50 chunks (EN + ID pairs)  
**Total for all 8 tracks:** ~360–400 chunks  
**Estimated embedding cost at launch (text-embedding-3-small):** < $1.00 one-time

---

## Remaining tracks to populate

| Track | Status |
|---|---|
| Backend Engineer | ✅ Complete (reference) |
| Frontend Engineer | ⬜ To do |
| DevOps / DevSecOps Engineer | ⬜ To do |
| ML / AI Engineer | ⬜ To do |
| UI/UX Designer | ⬜ To do |
| Digital Marketer | ⬜ To do |
| Cybersecurity Analyst | ⬜ To do |
| Data Analyst | ⬜ To do |

---

# USER RAG — What to Store & How to Structure It

Unlike the Knowledge RAG (shared, curated, static), the User RAG is personal and dynamic. Every user has their own isolated vector store. Here is exactly what gets embedded and how each chunk should be structured.

---

## User RAG Chunk Types

### Type 1: Profile snapshot

Embedded once on onboarding, re-embedded on profile update.

```
Content to embed:
"[User name] is a [current_role] with [years_experience] years of experience in [current_field].
Current skills: [skill list]. Target role: [target_role] in [time_horizon].
Gap score: [gap_score]. Daily study budget: [time_budget] minutes.
Preferred learning style: [style]. Best study time: [preferred_study_time].
Main blockers: [blockers]."

Metadata:
{
  "type": "profile",
  "updated_at": "ISO timestamp"
}
```

### Type 2: Activity log entry

Embedded after every Logging Classifier run.

```
Content to embed:
"[date]: Studied [classified_skill]. Source: [source_type].
Topics covered: [extracted_topics joined by comma].
Duration: [duration_minutes] minutes.
Mapped to milestone: [milestone title].
Skill level signal: [skill_level_signal]."

Metadata:
{
  "type": "activity_log",
  "log_id": "uuid",
  "milestone_id": "m003",
  "skill": "Operating Systems",
  "logged_at": "ISO timestamp"
}
```

### Type 3: Milestone completion event

Embedded when a milestone reaches 100% progress.

```
Content to embed:
"[date]: Completed milestone '[milestone_title]' in Phase [phase_number] ([phase_title]).
This milestone covered: [milestone description].
Time taken: [actual_weeks] weeks. Target was [planned_weeks] weeks."

Metadata:
{
  "type": "milestone_completion",
  "milestone_id": "uuid",
  "phase_number": 1,
  "completed_at": "ISO timestamp"
}
```

### Type 4: Focus session summary

Embedded after each completed Pomodoro session.

```
Content to embed:
"[date] [time]: Completed [duration_minutes]-minute focus session.
Task: [task_title]. Verified by photo: [yes/no].
Part of milestone: [milestone_title]."

Metadata:
{
  "type": "focus_session",
  "session_id": "uuid",
  "task_id": "t001",
  "verified": true,
  "logged_at": "ISO timestamp"
}
```

### Type 5: User note

Embedded when user saves a note from the Overview tab.

```
Content to embed:
Raw note text as-is. No transformation needed.

Metadata:
{
  "type": "note",
  "note_id": "uuid",
  "created_at": "ISO timestamp"
}
```

### Type 6: Weekly behavioral summary

Generated every Sunday by a cron job. Summarizes the week's patterns — not just what was studied but when and how consistently.

```
Content to embed:
"Week of [date range]: Logged [total_sessions] study sessions totaling [total_minutes] minutes.
Skills practiced: [list]. Most active day: [day]. Streak at end of week: [streak].
Milestones progressed: [list]. Notes saved: [count].
Consistency: [X of 7 days active]."

Metadata:
{
  "type": "weekly_summary",
  "week_start": "ISO date",
  "week_end": "ISO date"
}
```

### Type 7: AI conversation summary

Generated every 7 days, summarizing key exchanges between user and AI. Not raw transcripts — summaries only, to keep token count manageable.

```
Content to embed:
"AI conversation summary ([date range]): User asked about [topics].
Key insights discussed: [summary]. Roadmap adjustments suggested: [if any].
User's expressed concerns: [if any]."

Metadata:
{
  "type": "conversation_summary",
  "period_start": "ISO date",
  "period_end": "ISO date"
}
```

---

## User RAG Query Patterns

| User question | Query strategy |
|---|---|
| "What did I study last month?" | Embed question → retrieve top-8 `activity_log` chunks filtered by `logged_at > 30 days ago` |
| "Am I on track?" | Retrieve top-5 `milestone_completion` + top-3 `weekly_summary` chunks → pass to Roadmap Agent |
| "Remember when I struggled with recursion?" | Pure semantic search across all chunk types — no metadata filter |
| Weekly recap generation | Filter `type IN (activity_log, focus_session, milestone_completion)` + `logged_at > 7 days ago` → summarize |
| Personalized daily quote | Retrieve most recent `activity_log` or `milestone_completion` chunk → generate quote grounded in actual progress |
| Monday briefing | Retrieve last `weekly_summary` + upcoming milestone tasks from SQL → combine |

---

*This document is the source of truth for Knowledge RAG content structure and User RAG embedding strategy. Engineering and content teams should both reference it.*
