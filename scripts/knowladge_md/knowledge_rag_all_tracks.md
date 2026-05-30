# Knowledge RAG — Remaining 7 Tracks
### Kaix · Career Knowledge Base
**Version:** 1.0  
**Tracks covered:** Frontend Engineer · DevOps Engineer · ML/AI Engineer · UI/UX Designer · Digital Marketer · Cybersecurity Analyst · Data Analyst  
**Format:** Same chunk structure as Backend Engineer reference track

> Backend Engineer track is in `knowledge_rag_template.md`. This file contains all remaining tracks. Together they form the complete Knowledge RAG content.

---

---

# TRACK: Frontend Engineer

---

## 1. Role Definition

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "en",
  "tags": ["role", "overview", "frontend", "what-is"]
}
```
### Content
A Frontend Engineer builds everything a user sees and interacts with in a web application. They are responsible for translating design mockups into functional, responsive, accessible interfaces — and for making those interfaces feel fast, smooth, and intuitive. Unlike backend engineers who work on invisible server logic, frontend engineers work on the visible layer: every button, form, animation, and page layout.

Day-to-day work involves writing HTML, CSS, and JavaScript, building reusable UI components, fetching and displaying data from backend APIs, optimizing page performance, ensuring cross-browser compatibility, and collaborating closely with UI/UX designers and backend engineers. Modern frontend engineering heavily involves component-based frameworks (React, Vue, Angular), TypeScript, and build tooling.

The role has evolved significantly. A modern senior frontend engineer is expected to understand performance profiling, accessibility standards, state management patterns, server-side rendering, and basic DevOps for deployment pipelines. The gap between "web developer who writes HTML" and "senior frontend engineer" is large and takes years of deliberate practice.

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "id",
  "tags": ["role", "overview", "frontend", "what-is"]
}
```
### Content
Frontend Engineer membangun semua yang dilihat dan diinteraksikan pengguna dalam aplikasi web. Mereka bertanggung jawab menerjemahkan desain menjadi antarmuka yang fungsional, responsif, dan mudah diakses — serta memastikan antarmuka terasa cepat, mulus, dan intuitif.

Pekerjaan sehari-hari meliputi: menulis HTML, CSS, dan JavaScript, membangun komponen UI yang dapat digunakan ulang, mengambil dan menampilkan data dari API backend, mengoptimasi performa halaman, memastikan kompatibilitas lintas browser, dan berkolaborasi erat dengan desainer UI/UX serta backend engineer.

Frontend engineering modern sangat bergantung pada framework berbasis komponen (React, Vue, Angular), TypeScript, dan build tooling. Engineer senior diharapkan memahami performance profiling, standar aksesibilitas, state management, server-side rendering, dan pipeline deployment dasar.

---

## 2. Seniority Levels

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "en",
  "tags": ["seniority", "levels", "career-ladder"]
}
```
### Content
**Junior Frontend Engineer (0–2 years)**
Implements UI from design specs. Writes HTML, CSS, basic JavaScript. Understands responsive layouts and basic component structure. Works under guidance. Typical tasks: building static pages, implementing designs pixel-perfect, fixing styling bugs.

**Mid-level Frontend Engineer (2–5 years)**
Works independently on features. Comfortable with a major framework (React/Vue). Understands state management, API integration, and component architecture. Writes tests. Typical tasks: building complete features, optimizing performance, mentoring juniors informally, reviewing pull requests.

**Senior Frontend Engineer (5–8 years)**
Leads technical design for frontend systems. Makes architectural decisions (state management approach, rendering strategy, component library structure). Defines standards and patterns. Deep expertise in performance, accessibility, and developer experience. Typical tasks: system design, technical mentoring, cross-team API contracts, performance audits.

**Lead / Staff Frontend Engineer (8+ years)**
Sets frontend architecture direction across multiple teams or products. Deep expertise in build systems, performance at scale, and developer tooling. Bridges product, design, and engineering at an organizational level.

---

## 3. Skill Taxonomy

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "skill_taxonomy",
  "seniority": "beginner",
  "language": "en",
  "tags": ["skill-order", "foundations", "beginner"]
}
```
### Content
**Phase 1 — Foundations (must learn in this order)**

1. **HTML** — Semantic markup, document structure, forms, tables, media elements. The literal skeleton of every web page. Cannot skip.
2. **CSS** — Box model, flexbox, grid, positioning, typography, colors, responsive design with media queries. Cannot build anything without this.
3. **JavaScript fundamentals** — Variables, functions, DOM manipulation, events, fetch API, async/await, ES6+ syntax. The language of interactivity.
4. **Git & GitHub** — Version control, branches, pull requests. Required for any collaborative codebase.
5. **Responsive design** — Mobile-first approach, breakpoints, fluid layouts. Every site must work on phones.
6. **Browser developer tools** — Inspect element, console, network tab, performance profiler. Your most-used debugging environment.
7. **npm & package management** — Installing and managing frontend dependencies. Required for modern tooling.
8. **Basic accessibility** — Semantic HTML, alt text, keyboard navigation, ARIA basics. Not optional — it's a legal requirement in many markets and the right thing to do.

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "skill_taxonomy",
  "seniority": "junior",
  "language": "en",
  "tags": ["skill-order", "junior-to-mid"]
}
```
### Content
**Phase 2 — Junior to Mid (requires Phase 1 complete)**

1. **React (or Vue.js)** — Component-based thinking, JSX, props, state, lifecycle, hooks (useState, useEffect, useContext). The most important framework skill for Indonesian job market.
2. **TypeScript** — Static typing, interfaces, generics. Now expected at most mid-level+ positions.
3. **State management** — Context API, then Zustand or Redux Toolkit. Understanding when and why to use global state.
4. **API integration** — Fetching from REST APIs, handling loading and error states, Axios or fetch with proper error handling.
5. **CSS frameworks** — Tailwind CSS (dominant in 2026) or CSS Modules. Writing scalable styles at component level.
6. **Testing basics** — Vitest or Jest for unit tests, React Testing Library for component tests. Minimum 60% coverage target.
7. **Build tooling** — Vite (primary in 2026), understanding what bundlers do, optimizing bundle size.
8. **Next.js basics** — File-based routing, server-side rendering vs static generation, the App Router. Expected at most mid-level React positions.

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "skill_taxonomy",
  "seniority": "mid",
  "language": "en",
  "tags": ["skill-order", "mid-to-senior", "advanced"]
}
```
### Content
**Phase 3 — Mid to Senior**

1. **Performance optimization** — Core Web Vitals (LCP, FID, CLS), code splitting, lazy loading, image optimization, bundle analysis, caching strategies.
2. **Advanced React patterns** — Compound components, render props, custom hooks architecture, performance optimization with useMemo/useCallback/React.memo.
3. **Server components & modern rendering** — React Server Components, streaming SSR, hydration, edge computing. The frontier of modern React.
4. **Accessibility mastery** — WCAG 2.1 AA compliance, screen reader testing, keyboard navigation audits, color contrast tools. Senior engineers own this.
5. **Design systems** — Building and maintaining a component library, design token management, documentation with Storybook.
6. **Animation & motion** — Framer Motion or GSAP, CSS animations, physics-based motion, accessibility considerations for reduced motion.
7. **Frontend architecture** — Micro-frontends, monorepo structure (Turborepo/Nx), module federation, caching strategies.
8. **Cross-browser & cross-device testing** — BrowserStack, real device testing, progressive enhancement strategies.

---

## 4. Milestone Templates

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "milestone_template",
  "seniority": "beginner",
  "language": "en",
  "tags": ["milestone", "phase-1", "foundations"]
}
```
### Content
**Milestone: HTML & CSS Mastery**
Duration: 4–6 weeks at 1hr/day
- Build 5 different page layouts from scratch (no frameworks): landing page, blog post, product card grid, navigation with dropdown, contact form
- All layouts must be fully responsive (mobile, tablet, desktop)
- Use semantic HTML throughout (header, main, nav, article, section, footer — not just divs)
- Signal: given any design mockup, can implement it in HTML/CSS in under 2 hours without looking anything up

**Milestone: JavaScript Fundamentals**
Duration: 6–8 weeks at 1hr/day
- Build an interactive todo app without any framework — just vanilla JS DOM manipulation
- Fetch data from a public API (e.g. JSONPlaceholder) and display it dynamically
- Implement a simple shopping cart with add/remove/total calculation
- Signal: can explain the event loop, explain async/await vs callbacks, and debug a JS error without help

**Milestone: First React App**
Duration: 4–6 weeks
- Build a complete CRUD app in React: notes app, bookmark manager, or habit tracker
- Must use: components, props, useState, useEffect, API calls, form handling
- Deploy to Vercel or Netlify
- Signal: can build a multi-page React app with routing and API integration independently

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "milestone_template",
  "seniority": "junior",
  "language": "en",
  "tags": ["milestone", "phase-2", "junior-to-mid"]
}
```
### Content
**Milestone: TypeScript + State Management**
Duration: 4–6 weeks
- Migrate an existing JavaScript React project to TypeScript
- Add proper interfaces for all props and API responses
- Implement Zustand or Redux Toolkit for global state
- Signal: can type a complex React component with confidence, no `any` types

**Milestone: Production-grade Next.js App**
Duration: 6–8 weeks
- Build a full Next.js application with: SSR pages, static pages, API routes, proper error boundaries, loading states
- Implement authentication (NextAuth or Supabase)
- Achieve 90+ Lighthouse performance score
- Signal: understands when to use SSR vs SSG vs CSR and why, can explain the tradeoffs

---

## 5. Resources

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "resource",
  "skill_name": "HTML & CSS",
  "seniority": "beginner",
  "language": "id",
  "tags": ["resource", "html", "css", "beginner", "indonesia"]
}
```
### Content
**Sumber belajar HTML & CSS untuk pemula**

Gratis & Bahasa Indonesia:
- Dicoding "Belajar Dasar Pemrograman Web" — struktur HTML, CSS, dan layout dasar. Gratis, bersertifikat, kurikulum jelas. Titik awal terbaik.
- Dicoding "Belajar Membuat Front-End Web untuk Pemula" — lanjutan, layout responsif, flexbox, grid.
- YouTube: Web Programming UNPAS (Sandhika Galih) — tutorial HTML/CSS Bahasa Indonesia paling komprehensif dan konsisten di YouTube ID.

Bahasa Inggris (untuk yang sudah cukup nyaman):
- The Odin Project (theodinproject.com) — gratis, project-based, sangat terstruktur. Salah satu kurikulum frontend terbaik yang ada.
- CSS-Tricks (css-tricks.com) — referensi teknis, terutama untuk flexbox dan grid.
- MDN Web Docs — dokumentasi resmi HTML/CSS. Bookmark dan gunakan sebagai referensi setiap hari.

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "resource",
  "skill_name": "React",
  "seniority": "junior",
  "language": "en",
  "tags": ["resource", "react", "junior"]
}
```
### Content
**Resources for learning React**

Official: React documentation (react.dev) — completely rewritten in 2023, now excellent and project-based. Start here before any course.

Courses:
- "React - The Complete Guide" by Maximilian Schwarzmüller (Udemy) — the most comprehensive React course available. Covers hooks, context, Redux, Next.js. Highly rated.
- Dicoding "Belajar Fundamental Aplikasi Web dengan React" — Bahasa Indonesia, structured curriculum, has certification. Good for Indonesian learners.

YouTube:
- Fireship (YouTube) — short, dense, excellent mental models for React concepts
- Web Dev Simplified — practical React tutorials, good explanation style
- Kevin Powell — CSS fundamentals alongside React, essential pairing

Books: "Learning React" by Alex Banks — solid conceptual foundation before diving into large projects.

Practice: Build at least 3 projects from scratch before taking another course. Tutorial fatigue is real in frontend — build more, watch less.

---

## 6. Blocker Patterns

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "blocker_pattern",
  "skill_name": "CSS",
  "seniority": "beginner",
  "language": "en",
  "tags": ["blocker", "css", "layout", "recovery"]
}
```
### Content
**Blocker: CSS layout confusion (flexbox/grid)**

Symptom: The user understands basic CSS properties but gets confused when trying to center things, create multi-column layouts, or make things responsive. They end up using `position: absolute` everywhere or fighting with margins. Classic sign: their layouts work on desktop but break on mobile.

Root cause: CSS layout requires a mental shift from thinking about individual element properties to thinking about parent-child relationships and flow. Flexbox and Grid are container properties — most beginners apply them to the wrong element.

Recovery approach:
1. Stop building new things for 3 days. Spend 1 hour each day on flexboxfroggy.com (flexbox) and cssgridgarden.com (grid) — these games force the correct mental model through play.
2. Then rebuild one layout you previously struggled with using only flexbox — no absolute positioning.
3. Read "A Complete Guide to Flexbox" on CSS-Tricks. Print it or bookmark it. This is your reference for the next 6 months.
4. Rule to remember: flexbox for one direction (row or column), grid for two dimensions (rows AND columns simultaneously).

Signal of recovery: Can center a div both horizontally and vertically in under 60 seconds, and can explain why the approach works.

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "blocker_pattern",
  "skill_name": "tutorial hell",
  "seniority": "beginner",
  "language": "id",
  "tags": ["blocker", "tutorial-hell", "procrastination", "recovery"]
}
```
### Content
**Blocker: Tutorial hell — menonton tanpa membangun**

Gejala: Pengguna sudah menonton puluhan jam tutorial React atau JavaScript, tapi ketika diminta membangun sesuatu sendiri dari nol, mereka bingung harus mulai dari mana. Mereka terus mencari tutorial baru daripada membangun sendiri.

Penyebab: Menonton coding bukan sama dengan coding. Tutorial memberikan ilusi kemampuan — kamu melihat hasilnya dan merasa paham, tapi otak tidak menyimpan kemampuan itu karena tidak ada perjuangan aktif.

Strategi pemulihan:
1. Stop menonton tutorial selama 2 minggu penuh. Tidak ada pengecualian.
2. Pilih satu project kecil yang bisa diselesaikan dalam 2 hari: todo app, kalkulator, quiz sederhana.
3. Bangun dari nol. Ketika stuck, google dulu selama 30 menit sebelum melihat tutorial.
4. Ketika benar-benar butuh referensi, baca dokumentasi (MDN, React docs) — bukan video.
5. Selesaikan project itu sampai bisa digunakan, bukan sampai sempurna.

Tanda pemulihan: Berhasil menyelesaikan satu project dari nol, meskipun kodenya jelek. Kode jelek yang jalan lebih berharga dari tutorial yang bagus yang tidak menghasilkan apa-apa.

---

## 7. Salary Context

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "salary_context",
  "seniority": "all",
  "language": "en",
  "tags": ["salary", "indonesia", "compensation"]
}
```
### Content
**Frontend Engineer compensation — Indonesian market (2026)**

| Level | Jakarta (IDR/month) | Remote SEA (USD/month) |
|---|---|---|
| Junior (0–2yr) | Rp 5–10 juta | $700–1,400 |
| Mid-level (2–5yr) | Rp 10–22 juta | $1,400–3,200 |
| Senior (5–8yr) | Rp 22–45 juta | $3,200–6,500 |
| Lead/Staff (8yr+) | Rp 45–90 juta | $6,500–14,000 |

Premium skills: React + TypeScript (standard expectation at mid+), Next.js, performance optimization experience, design system ownership. Engineers who can also handle basic DevOps (CI/CD, Vercel deployment) command 10–15% premium.

Frontend engineers in Indonesian product companies (Gojek, Tokopedia, Traveloka, Shopee ID) typically earn 20–40% above market average.

---

## 8. Career Transitions

---chunk---
### Metadata
```json
{
  "career_track": "frontend_engineer",
  "content_type": "career_transition",
  "seniority": "all",
  "language": "en",
  "tags": ["transition", "from", "career-change"]
}
```
### Content
**Common paths into Frontend Engineering**

**From UI/UX Designer:** The most natural transition. Already understands user needs, design principles, and visual hierarchy. Needs to learn: HTML/CSS (often partially known), JavaScript, and React. The biggest mental shift is from visual to logical thinking. Typical time: 4–8 months.

**From Backend Engineer:** Already knows JavaScript (if Node.js), Git, APIs. Needs to learn: CSS layout, component thinking, user experience considerations. Often underestimates how much depth CSS requires. Typical time: 3–6 months.

**From Complete Beginner:** Start with HTML → CSS → JavaScript → React in sequence. No shortcuts. Typical time to junior-ready: 8–14 months of consistent practice.

**Frontend to adjacent roles:**
- Frontend → Full-stack: add Node.js, databases, APIs (4–8 months)
- Frontend → UI/UX: add design tools, user research methods (6–12 months)
- Frontend → Mobile (React Native): add native concepts, app store processes (3–6 months)

---

---

# TRACK: DevOps Engineer

---

## 1. Role Definition

---chunk---
### Metadata
```json
{
  "career_track": "devops_engineer",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "en",
  "tags": ["role", "overview", "devops", "what-is"]
}
```
### Content
A DevOps Engineer bridges the gap between software development and IT operations. They are responsible for building and maintaining the infrastructure, automation pipelines, and tooling that allow development teams to ship software reliably, quickly, and safely. The core philosophy of DevOps is eliminating the friction between "building code" and "running code in production."

Day-to-day work involves: designing and maintaining CI/CD pipelines, managing cloud infrastructure (AWS, GCP, or Azure), containerizing applications with Docker and orchestrating them with Kubernetes, implementing monitoring and alerting systems, automating repetitive operational tasks with scripts and Infrastructure as Code (Terraform), and responding to production incidents.

DevOps is one of the most in-demand and highest-paying engineering tracks in 2026. The shift toward cloud-native architectures, microservices, and AI/ML workloads has made skilled DevOps and Platform engineers essential at every technology company. In Indonesia, the shortage of qualified DevOps engineers means mid-to-senior practitioners command significantly above-market salaries.

---chunk---
### Metadata
```json
{
  "career_track": "devops_engineer",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "id",
  "tags": ["role", "overview", "devops", "what-is"]
}
```
### Content
DevOps Engineer menjembatani kesenjangan antara pengembangan software dan operasi IT. Mereka bertanggung jawab membangun dan memelihara infrastruktur, pipeline otomasi, dan tooling yang memungkinkan tim development untuk mengirimkan software secara andal, cepat, dan aman.

Pekerjaan sehari-hari meliputi: merancang dan memelihara pipeline CI/CD, mengelola infrastruktur cloud (AWS, GCP, atau Azure), mengontainerisasi aplikasi dengan Docker dan mengorkestrasikannya dengan Kubernetes, mengimplementasikan sistem monitoring dan alerting, mengotomasi tugas-tugas operasional berulang dengan skrip dan Infrastructure as Code (Terraform), serta merespons insiden produksi.

DevOps adalah salah satu track engineering yang paling diminati dan bergaji tinggi di 2026. Di Indonesia, kekurangan DevOps engineer yang qualified membuat praktisi mid-to-senior mendapatkan gaji jauh di atas rata-rata pasar.

---

## 2. Skill Taxonomy

---chunk---
### Metadata
```json
{
  "career_track": "devops_engineer",
  "content_type": "skill_taxonomy",
  "seniority": "beginner",
  "language": "en",
  "tags": ["skill-order", "foundations", "beginner"]
}
```
### Content
**Phase 1 — Foundations**

1. **Linux command line** — File system navigation, permissions, processes, networking commands (curl, netstat, ss), text processing (grep, awk, sed). The foundation of everything. Must be deeply comfortable here.
2. **Bash scripting** — Variables, loops, conditionals, functions, error handling. Automate repetitive tasks. A DevOps engineer who can't script is not a DevOps engineer.
3. **Git & version control** — Branching strategies, rebasing, merge conflicts, tagging, hooks. DevOps requires deeper Git knowledge than most developers.
4. **Networking fundamentals** — TCP/IP, DNS, HTTP/HTTPS, load balancing, firewalls, VPNs, subnets. Cannot manage cloud infrastructure without this.
5. **Docker** — Containerization concepts, writing Dockerfiles, docker-compose, image registries (Docker Hub, ECR). The gateway to cloud-native work.
6. **One cloud provider basics** — Start with AWS (most jobs) or GCP (growing in ID). EC2/Compute, S3/Cloud Storage, IAM, VPC, RDS. Get the cloud provider's associate-level certification.
7. **Python or Go basics** — For writing automation scripts and tools. Python is faster to learn; Go produces faster tools. Python is sufficient for most DevOps work.

---chunk---
### Metadata
```json
{
  "career_track": "devops_engineer",
  "content_type": "skill_taxonomy",
  "seniority": "junior",
  "language": "en",
  "tags": ["skill-order", "junior-to-mid"]
}
```
### Content
**Phase 2 — Junior to Mid**

1. **Kubernetes (K8s)** — Pod, Deployment, Service, Ingress, ConfigMap, Secret, Helm charts, kubectl. The most in-demand DevOps skill. Start with Minikube locally, then managed K8s (EKS/GKE).
2. **CI/CD pipelines** — GitHub Actions (primary 2026), GitLab CI, or Jenkins. Building pipelines that test, build, and deploy automatically on every commit.
3. **Terraform (Infrastructure as Code)** — Writing declarative infrastructure, state management, modules, workspaces. Treating infrastructure like software code.
4. **Monitoring & observability** — Prometheus for metrics, Grafana for dashboards, Loki for logs, OpenTelemetry for tracing. Building systems that tell you when something is wrong.
5. **Security basics** — Secrets management (HashiCorp Vault, AWS Secrets Manager), least-privilege IAM, network security groups, container scanning.
6. **Database operations** — Backup strategies, replication, failover, performance monitoring. DevOps engineers own database reliability.
7. **On-call & incident response** — Runbooks, post-mortem culture, SLIs/SLOs/SLAs. Learning to handle production incidents calmly.

---chunk---
### Metadata
```json
{
  "career_track": "devops_engineer",
  "content_type": "skill_taxonomy",
  "seniority": "mid",
  "language": "en",
  "tags": ["skill-order", "mid-to-senior", "advanced"]
}
```
### Content
**Phase 3 — Mid to Senior**

1. **Platform engineering** — Building internal developer platforms (IDPs), self-service infrastructure, golden path templates. The next evolution of DevOps.
2. **Service mesh** — Istio or Linkerd for microservice communication, mTLS, traffic management, observability.
3. **GitOps** — ArgoCD or Flux for declarative, Git-driven deployments. Modern Kubernetes deployment standard.
4. **Cost optimization** — FinOps principles, rightsizing, spot/preemptible instances, reserved capacity planning. Cloud costs are a major engineering concern.
5. **Disaster recovery & resilience** — Multi-region deployments, chaos engineering (Chaos Monkey principles), RTO/RPO planning.
6. **Advanced Kubernetes** — Custom operators, admission webhooks, cluster federation, multi-tenant architectures.
7. **MLOps** — Serving ML models, managing GPU workloads, ML pipeline orchestration (Kubeflow, MLflow). Growing demand in Indonesian tech companies.

---

## 3. Milestone Templates

---chunk---
### Metadata
```json
{
  "career_track": "devops_engineer",
  "content_type": "milestone_template",
  "seniority": "beginner",
  "language": "en",
  "tags": ["milestone", "phase-1", "foundations"]
}
```
### Content
**Milestone: Linux & Docker Comfortable**
Duration: 6–8 weeks at 1hr/day
- Navigate any Linux filesystem, manage processes, configure basic networking — without Googling
- Write a Bash script that automates a real repetitive task (file cleanup, log rotation, deployment step)
- Containerize a simple web app: write Dockerfile, build image, run container, expose port
- Use docker-compose to run a multi-service local environment (app + database + cache)
- Signal: can SSH into a Linux server, diagnose a running application's issues, and containerize it — all without help

**Milestone: CI/CD Pipeline in Production**
Duration: 4–6 weeks
- Build a GitHub Actions pipeline for a real project: lint → test → build → deploy
- Pipeline must block merges if tests fail
- Deploy to a cloud provider (AWS, GCP, or Vercel/Railway for starters)
- Signal: every code change triggers automated tests and deploys automatically — you never manually FTP a file again

---chunk---
### Metadata
```json
{
  "career_track": "devops_engineer",
  "content_type": "milestone_template",
  "seniority": "junior",
  "language": "en",
  "tags": ["milestone", "phase-2", "junior-to-mid"]
}
```
### Content
**Milestone: Kubernetes Cluster Running**
Duration: 8–10 weeks
- Deploy a multi-service application on Kubernetes (at least: app + database + cache)
- Write proper Deployments, Services, ConfigMaps, Secrets, and Ingress
- Set up Helm chart for the application
- Configure horizontal pod autoscaling based on CPU/memory
- Signal: application survives pod restarts, scales automatically under load, secrets are not in plaintext anywhere

**Milestone: Full Observability Stack**
Duration: 4–6 weeks
- Deploy Prometheus + Grafana on the Kubernetes cluster
- Create dashboards for: request rate, error rate, latency (RED method), infrastructure metrics
- Set up alerts for: pod crash loops, high CPU, high error rate, disk space
- Write a runbook for the top 3 most likely incidents
- Signal: if the production system goes down at 2am, you have enough visibility to diagnose and fix within 30 minutes

---

## 4. Resources

---chunk---
### Metadata
```json
{
  "career_track": "devops_engineer",
  "content_type": "resource",
  "skill_name": "Kubernetes",
  "seniority": "junior",
  "language": "en",
  "tags": ["resource", "kubernetes", "docker", "cloud"]
}
```
### Content
**Resources for DevOps & Kubernetes**

Courses:
- "Docker & Kubernetes: The Practical Guide" (Udemy, Maximilian Schwarzmüller) — 4.7★, 23 hours. Best single course combining Docker and Kubernetes.
- "Certified Kubernetes Administrator (CKA)" prep courses — Killer.sh practice exams are essential.
- Dicoding "Belajar Membangun Arsitektur Microservices" — Bahasa Indonesia, covers container orchestration fundamentals.
- "HashiCorp Terraform Associate" Udemy courses — Terraform is non-negotiable at mid-level.

Free resources:
- Kubernetes official documentation (kubernetes.io/docs) — comprehensive, well-maintained.
- "The DevOps Handbook" (Gene Kim et al.) — the philosophy behind DevOps, not just tooling.
- roadmap.sh/devops — visual skill map showing what to learn and in what order.
- KodeKloud — hands-on DevOps labs, browser-based. Excellent for practicing without cloud spend.

Certifications worth getting (in order):
1. AWS Certified Solutions Architect Associate (or GCP equivalent) — foundational cloud
2. Certified Kubernetes Administrator (CKA) — validates K8s depth
3. HashiCorp Terraform Associate — validates IaC skills

---

## 5. Blocker Patterns

---chunk---
### Metadata
```json
{
  "career_track": "devops_engineer",
  "content_type": "blocker_pattern",
  "skill_name": "Kubernetes complexity",
  "seniority": "junior",
  "language": "en",
  "tags": ["blocker", "kubernetes", "complexity", "recovery"]
}
```
### Content
**Blocker: Kubernetes feels overwhelming**

Symptom: The user understands Docker but feels completely lost in Kubernetes. There are too many concepts (Pods, ReplicaSets, Deployments, Services, Ingress, ConfigMaps, Secrets, Namespaces, RBAC...) and they don't know how they connect. They try to follow tutorials but feel like they're copying commands without understanding.

Root cause: Kubernetes has a steep learning curve because it introduces many abstractions simultaneously. Most tutorials jump straight to complex manifests without building the mental model first.

Recovery approach:
1. Stop tutorials. Spend 2 days just playing with a local cluster (Minikube or Kind). Create and delete Pods manually. Break things. Read error messages.
2. Internalize one core insight: Kubernetes is a desired-state machine. You tell it what you want (a YAML file) and it constantly tries to make reality match that desire. Every concept (ReplicaSet, Deployment, etc.) is just a layer on top of this one idea.
3. Follow this learning order: Pod → ReplicaSet (why Pods alone aren't enough) → Deployment (why ReplicaSets alone aren't enough) → Service (how to reach Pods) → Ingress (how the outside world reaches Services).
4. Build one real application on Kubernetes before moving to advanced topics.

Signal of recovery: Can explain what happens step-by-step when a Pod crashes and why Kubernetes automatically restarts it.

---

## 6. Salary Context

---chunk---
### Metadata
```json
{
  "career_track": "devops_engineer",
  "content_type": "salary_context",
  "seniority": "all",
  "language": "id",
  "tags": ["salary", "indonesia", "compensation"]
}
```
### Content
**Kompensasi DevOps Engineer — Pasar Indonesia (2026)**

| Level | Jakarta (IDR/bulan) | Remote SEA (USD/bulan) |
|---|---|---|
| Junior (0–2thn) | Rp 8–15 juta | $1,000–1,800 |
| Mid-level (2–5thn) | Rp 15–30 juta | $1,800–4,000 |
| Senior (5–8thn) | Rp 30–60 juta | $4,000–8,000 |
| Lead/Staff (8thn+) | Rp 60–120 juta | $8,000–16,000+ |

DevOps adalah salah satu track dengan shortage talent terbesar di Indonesia. Engineer dengan kombinasi Kubernetes + AWS/GCP + Terraform + CI/CD sangat langka dan bisa bernegosiasi gaji secara agresif. Sertifikasi CKA dan AWS SAA meningkatkan nilai kompensasi secara signifikan — perusahaan besar sering memberikan bonus sertifikasi tambahan.

---

---

# TRACK: ML / AI Engineer

---

## 1. Role Definition

---chunk---
### Metadata
```json
{
  "career_track": "ml_ai_engineer",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "en",
  "tags": ["role", "overview", "machine-learning", "ai", "what-is"]
}
```
### Content
An ML/AI Engineer designs, trains, deploys, and maintains machine learning models and AI systems. Unlike a Data Scientist who focuses on analysis and insights, an ML Engineer focuses on building production-ready AI systems — systems that can run at scale, handle real data, and be maintained over time.

Day-to-day work involves: processing and cleaning large datasets, designing and training machine learning models, evaluating model performance, deploying models as APIs or integrated services, monitoring model drift and retraining, building ML pipelines, and working with LLMs (Large Language Models) for AI applications. In 2026, a large portion of ML/AI engineering work involves building applications on top of existing foundation models (GPT-4, Claude, Gemini) using RAG, fine-tuning, and agentic frameworks.

This is the fastest-growing engineering track globally in 2026. Indonesia is experiencing significant demand from fintech, healthtech, e-commerce, and government sectors — all seeking to integrate AI into their products and operations.

---chunk---
### Metadata
```json
{
  "career_track": "ml_ai_engineer",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "id",
  "tags": ["role", "overview", "machine-learning", "ai", "what-is"]
}
```
### Content
ML/AI Engineer merancang, melatih, menerapkan, dan memelihara model machine learning dan sistem AI. Berbeda dengan Data Scientist yang berfokus pada analisis dan wawasan, ML Engineer berfokus pada membangun sistem AI yang siap produksi — sistem yang dapat berjalan dalam skala besar, menangani data nyata, dan dapat dipelihara dari waktu ke waktu.

Pekerjaan sehari-hari meliputi: memproses dan membersihkan dataset besar, merancang dan melatih model machine learning, mengevaluasi performa model, menerapkan model sebagai API atau layanan terintegrasi, memantau model drift dan melatih ulang, membangun pipeline ML, serta bekerja dengan LLM (Large Language Models) untuk aplikasi AI. Di 2026, sebagian besar pekerjaan ML/AI engineering melibatkan membangun aplikasi di atas model foundational yang sudah ada menggunakan RAG, fine-tuning, dan framework agentic.

---

## 2. Skill Taxonomy

---chunk---
### Metadata
```json
{
  "career_track": "ml_ai_engineer",
  "content_type": "skill_taxonomy",
  "seniority": "beginner",
  "language": "en",
  "tags": ["skill-order", "foundations", "beginner", "math"]
}
```
### Content
**Phase 1 — Foundations (mathematics-first)**

1. **Python proficiency** — Must be solid before anything else. NumPy, Pandas, Matplotlib are daily tools.
2. **Linear Algebra** — Vectors, matrices, matrix multiplication, eigenvalues. Every ML algorithm is linear algebra under the hood.
3. **Statistics & probability** — Mean, variance, distributions (normal, binomial, Poisson), hypothesis testing, Bayes' theorem, p-values. ML is applied statistics.
4. **Calculus basics** — Derivatives, chain rule, gradients. Gradient descent — the algorithm that trains every neural network — requires this.
5. **Data manipulation with Pandas** — Loading, cleaning, merging, transforming, aggregating datasets. Real data is messy — this is most of the job.
6. **Data visualization** — Matplotlib, Seaborn. Understanding your data visually before modeling it.
7. **Scikit-learn** — The standard Python ML library. Classification, regression, clustering, preprocessing, model evaluation, cross-validation.
8. **Git + Jupyter notebooks** — Version control for code; notebooks for exploratory analysis.

---chunk---
### Metadata
```json
{
  "career_track": "ml_ai_engineer",
  "content_type": "skill_taxonomy",
  "seniority": "junior",
  "language": "en",
  "tags": ["skill-order", "junior-to-mid", "deep-learning"]
}
```
### Content
**Phase 2 — Deep Learning & Production**

1. **Deep learning fundamentals** — Neural networks, backpropagation, activation functions, loss functions, optimizers (Adam, SGD). Understand what's happening inside the model, not just the API.
2. **PyTorch** — Primary framework for research and production in 2026. Build and train models from scratch before using high-level wrappers.
3. **Computer Vision basics** — CNNs, image classification, object detection (YOLO fundamentals). Many Indonesian ML jobs involve CV.
4. **NLP fundamentals** — Text preprocessing, embeddings, sequence models, transformers. Foundation for LLM work.
5. **Model evaluation** — Precision, recall, F1, ROC-AUC, confusion matrices, bias-variance tradeoff. Knowing what makes a model good or bad.
6. **Experiment tracking** — MLflow or Weights & Biases for logging runs, comparing models, reproducibility.
7. **FastAPI for model serving** — Deploying ML models as REST APIs. The bridge between data science and production engineering.
8. **Docker for ML** — Containerizing models with their dependencies. Required for deployment.

---chunk---
### Metadata
```json
{
  "career_track": "ml_ai_engineer",
  "content_type": "skill_taxonomy",
  "seniority": "mid",
  "language": "en",
  "tags": ["skill-order", "mid-to-senior", "llm", "mlops"]
}
```
### Content
**Phase 3 — LLMs, MLOps & Advanced Systems**

1. **LLM application development** — Prompt engineering, RAG (Retrieval-Augmented Generation), LangChain/LlamaIndex, vector databases (Pinecone, pgvector), fine-tuning. The dominant ML engineering work of 2026.
2. **Agentic AI systems** — Building AI agents with tool use, memory, multi-step reasoning. LangGraph, CrewAI, AutoGen. Rapidly growing demand.
3. **MLOps** — Full pipeline automation: data ingestion → preprocessing → training → evaluation → deployment → monitoring → retraining. Tools: Kubeflow, Airflow, Metaflow.
4. **Model monitoring & drift detection** — Detecting when model performance degrades in production, setting up alerting, automated retraining triggers.
5. **Large-scale training** — Distributed training, GPU cluster management, gradient checkpointing, mixed precision training.
6. **Responsible AI** — Bias detection, fairness metrics, model explainability (SHAP, LIME), regulatory compliance (GDPR/UU PDP for Indonesian market).
7. **GPU infrastructure** — CUDA basics, GPU memory management, serving optimization (TensorRT, ONNX).

---

## 3. Milestone Templates

---chunk---
### Metadata
```json
{
  "career_track": "ml_ai_engineer",
  "content_type": "milestone_template",
  "seniority": "beginner",
  "language": "en",
  "tags": ["milestone", "phase-1", "foundations"]
}
```
### Content
**Milestone: Classical ML Proficiency**
Duration: 8–10 weeks at 1hr/day
- Complete end-to-end ML project: data loading → EDA → preprocessing → model training → evaluation → conclusion
- Use at least 3 different algorithms on the same problem and compare results with proper metrics
- Submit to one Kaggle competition (finishing position doesn't matter — completing the process does)
- Signal: given a tabular dataset and a problem statement, can build and evaluate a baseline ML model independently

**Milestone: First Neural Network from Scratch**
Duration: 6–8 weeks
- Build a simple neural network using only NumPy (no PyTorch) — forces understanding of what the library does for you
- Then rebuild the same network in PyTorch
- Train on MNIST (image classification) and IMDB (sentiment analysis)
- Signal: can explain backpropagation, gradient descent, and why the learning rate matters — without looking anything up

---chunk---
### Metadata
```json
{
  "career_track": "ml_ai_engineer",
  "content_type": "milestone_template",
  "seniority": "junior",
  "language": "en",
  "tags": ["milestone", "phase-2", "deployment", "llm"]
}
```
### Content
**Milestone: ML Model in Production**
Duration: 6–8 weeks
- Train a custom model (classification, NLP, or CV) and deploy it as a FastAPI REST API
- Containerize with Docker, deploy to a cloud provider
- Add logging, error handling, and basic metrics
- Signal: someone else can call your model API and get predictions — it doesn't just run in a notebook

**Milestone: RAG Application Built**
Duration: 4–6 weeks
- Build a RAG (Retrieval-Augmented Generation) application: document ingestion → chunking → embedding → vector store → retrieval → LLM response
- Use pgvector or Pinecone, with an OpenAI or open-source LLM
- Add chat history, source citation, and basic evaluation
- Signal: the application gives accurate answers grounded in the provided documents, with source references

---

## 4. Resources

---chunk---
### Metadata
```json
{
  "career_track": "ml_ai_engineer",
  "content_type": "resource",
  "skill_name": "machine learning",
  "seniority": "beginner",
  "language": "id",
  "tags": ["resource", "machine-learning", "indonesia", "beginner"]
}
```
### Content
**Sumber belajar ML/AI untuk pemula (Bahasa Indonesia)**

Gratis:
- Dicoding "Machine Learning Developer" learning path — kurikulum terstruktur dari Dicoding, mencakup fundamental hingga deployment. Bersertifikat, Bahasa Indonesia.
- rubythalib.ai Academy — kelas Computer Vision dan NLP berbasis PyTorch/TensorFlow dari praktisi Indonesia. Sangat praktis dan kontekstual untuk pasar lokal.
- rubythalib.ai "Introduction to Machine Learning" — gratis di goakal.com, titik awal yang bagus.
- YouTube: rubythalib.ai channel — tutorial ML Indonesia yang praktikal.

Bahasa Inggris:
- "Hands-On Machine Learning" oleh Aurélien Géron — buku terbaik untuk ML practitioner. Covers scikit-learn, Keras, dan TensorFlow secara mendalam.
- Fast.ai (fast.ai) — gratis, top-down approach, langsung praktek dengan kasus nyata sebelum teori mendalam.
- Deep Learning Specialization (Andrew Ng, Coursera) — fondasi teori yang kuat untuk neural networks.
- LangChain documentation + tutorials — untuk LLM application development.

---

## 5. Salary Context

---chunk---
### Metadata
```json
{
  "career_track": "ml_ai_engineer",
  "content_type": "salary_context",
  "seniority": "all",
  "language": "en",
  "tags": ["salary", "indonesia", "compensation"]
}
```
### Content
**ML/AI Engineer compensation — Indonesian market (2026)**

| Level | Jakarta (IDR/month) | Remote SEA (USD/month) |
|---|---|---|
| Junior (0–2yr) | Rp 8–18 juta | $1,000–2,000 |
| Mid-level (2–5yr) | Rp 18–35 juta | $2,000–5,000 |
| Senior (5–8yr) | Rp 35–70 juta | $5,000–10,000 |
| Lead/Staff (8yr+) | Rp 70–150 juta | $10,000–20,000+ |

ML/AI Engineering is the highest-compensated track in Indonesian tech in 2026, driven by massive demand and very limited supply. Engineers with LLM application development experience, RAG system design, and production ML deployment skills are particularly sought after. Fintech (OVO, GoPay, Bank Jago), healthtech, and government AI initiatives are the primary employers.

---

---

# TRACK: UI/UX Designer

---

## 1. Role Definition

---chunk---
### Metadata
```json
{
  "career_track": "ui_ux_designer",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "en",
  "tags": ["role", "overview", "design", "ux", "ui", "what-is"]
}
```
### Content
A UI/UX Designer is responsible for creating digital experiences that are both useful and delightful. UX (User Experience) focuses on the structure, flow, and logic of a product — making sure users can accomplish their goals easily. UI (User Interface) focuses on the visual layer — the colors, typography, components, and visual hierarchy that communicate the experience.

In practice, most roles in Indonesia combine both. Day-to-day work involves: conducting user research, creating user journey maps and personas, wireframing and prototyping in Figma, conducting usability testing, building and maintaining design systems, writing design specifications for engineers, and collaborating with product managers and developers throughout the product development process.

The field is rapidly evolving in 2026. AI tools (Figma AI, Midjourney for moodboards, ChatGPT for UX copy) are augmenting designer workflows. Designers who understand frontend basics (HTML/CSS, React component thinking) are significantly more effective collaborators and are promoted faster. Strong portfolio work remains the primary hiring signal in this field — certificates matter less than demonstrated craft.

---chunk---
### Metadata
```json
{
  "career_track": "ui_ux_designer",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "id",
  "tags": ["role", "overview", "design", "ux", "ui", "what-is"]
}
```
### Content
UI/UX Designer bertanggung jawab menciptakan pengalaman digital yang berguna sekaligus menyenangkan. UX (User Experience) berfokus pada struktur, alur, dan logika produk — memastikan pengguna dapat mencapai tujuan mereka dengan mudah. UI (User Interface) berfokus pada lapisan visual — warna, tipografi, komponen, dan hierarki visual yang mengkomunikasikan pengalaman tersebut.

Pekerjaan sehari-hari meliputi: melakukan riset pengguna, membuat user journey map dan persona, membuat wireframe dan prototipe di Figma, melakukan usability testing, membangun dan memelihara design system, menulis spesifikasi desain untuk engineer, serta berkolaborasi dengan product manager dan developer sepanjang proses pengembangan produk.

Portofolio tetap menjadi sinyal hiring utama di bidang ini — sertifikat lebih sedikit berpengaruh dibanding karya yang terbukti berkualitas.

---

## 2. Skill Taxonomy

---chunk---
### Metadata
```json
{
  "career_track": "ui_ux_designer",
  "content_type": "skill_taxonomy",
  "seniority": "beginner",
  "language": "en",
  "tags": ["skill-order", "foundations", "beginner"]
}
```
### Content
**Phase 1 — Foundations**

1. **Design principles** — Visual hierarchy, contrast, alignment, proximity, repetition (CRAP principles). The grammar of visual design. Cannot skip.
2. **Typography** — Type scales, pairing fonts, line height, letter spacing, readability at different sizes. One of the most impactful skills in UI.
3. **Color theory** — Hue, saturation, value, color harmony, accessible color contrast (WCAG ratios), building a color system.
4. **Figma basics** — Frames, components, auto-layout, variants, styles, prototyping. Figma is the industry standard — master it deeply.
5. **User research basics** — User interviews, surveys, affinity mapping, personas. Understanding users before designing for them.
6. **Information architecture** — Card sorting, sitemaps, user flows. Organizing information so users can find what they need.
7. **Wireframing** — Low-fidelity sketches and mid-fidelity wireframes. Separating structure decisions from visual decisions.
8. **Mobile design patterns** — Bottom navigation, gestures, safe areas, platform conventions (iOS vs Android). Mobile-first is the standard in Indonesia.

---chunk---
### Metadata
```json
{
  "career_track": "ui_ux_designer",
  "content_type": "skill_taxonomy",
  "seniority": "junior",
  "language": "en",
  "tags": ["skill-order", "junior-to-mid"]
}
```
### Content
**Phase 2 — Mid-level Design**

1. **Figma advanced** — Component libraries, design tokens, variables, branching, dev mode. Deep Figma mastery separates good from great designers.
2. **Usability testing** — Moderated and unmoderated testing, writing test scripts, analyzing findings, communicating results to stakeholders.
3. **Design systems** — Atomic design methodology, building scalable component libraries, documentation, designer-developer handoff.
4. **Interaction design** — Micro-interactions, animation principles, motion design basics. When and why to animate things.
5. **Accessibility design** — Color contrast tools, focus states, touch target sizing, screen reader considerations. Often neglected, increasingly required.
6. **Product thinking** — Understanding business metrics, user goals vs business goals, success metrics for design decisions.
7. **HTML & CSS basics** — Not required, but designers who understand how browsers render layouts are significantly better at designer-developer collaboration and avoid designing impossible things.
8. **Presentation & storytelling** — Presenting design decisions with rationale, defending choices with data, persuading stakeholders.

---chunk---
### Metadata
```json
{
  "career_track": "ui_ux_designer",
  "content_type": "skill_taxonomy",
  "seniority": "mid",
  "language": "en",
  "tags": ["skill-order", "mid-to-senior", "advanced"]
}
```
### Content
**Phase 3 — Senior Design**

1. **Design strategy** — Vision documents, future-state design, connecting design decisions to business strategy.
2. **Design leadership** — Mentoring junior designers, establishing team processes, critique culture, design principles.
3. **Quantitative UX** — A/B testing, analytics (Mixpanel, Amplitude), cohort analysis, conversion rate optimization. Data-driven design decisions.
4. **Service design** — Designing across touchpoints (digital + physical + human), service blueprints, systemic thinking.
5. **Design ops** — Design team tooling, workflow standardization, scaling design processes, cross-team collaboration frameworks.
6. **Advanced prototyping** — Framer, ProtoPie, or high-fidelity Figma prototypes with complex interactions for user testing.

---

## 3. Milestone Templates

---chunk---
### Metadata
```json
{
  "career_track": "ui_ux_designer",
  "content_type": "milestone_template",
  "seniority": "beginner",
  "language": "en",
  "tags": ["milestone", "phase-1", "portfolio"]
}
```
### Content
**Milestone: First Portfolio Case Study**
Duration: 6–8 weeks
- Choose a real app or product with obvious UX problems (government apps, local business apps are great candidates)
- Conduct at least 3 user interviews about the problem
- Create journey map, identify pain points, define design goals
- Design a improved solution: wireframes → high-fidelity mockups in Figma → interactive prototype
- Write a case study documenting the process: problem → research → decisions → solution
- Signal: someone can read your case study and understand not just what you designed, but why you made each decision

**Milestone: Design System in Figma**
Duration: 4–5 weeks
- Build a complete design system from scratch: color palette, typography scale, spacing system, 20+ components with variants
- Document each component: usage guidelines, do/don't examples
- All components use auto-layout and are properly named
- Signal: another designer can use your design system and produce consistent designs without asking you questions

---

## 4. Resources & Salary

---chunk---
### Metadata
```json
{
  "career_track": "ui_ux_designer",
  "content_type": "resource",
  "skill_name": "Figma",
  "seniority": "beginner",
  "language": "id",
  "tags": ["resource", "figma", "ux", "indonesia", "beginner"]
}
```
### Content
**Sumber belajar UI/UX Design (Bahasa Indonesia)**

Gratis:
- Dicoding "Belajar Dasar UX Design" — dasar-dasar UX, riset pengguna, wireframing. Gratis, bersertifikat.
- Dicoding "Belajar Membuat Prototype Aplikasi" — prototyping dengan Figma, Bahasa Indonesia.
- YouTube: Malewang Design, DesignSkilz — konten desain Indonesia berkualitas.
- Figma Community — template dan design system gratis untuk dipelajari dan di-fork.

Berbayar:
- Buildwithangga.com — platform kursus desain Indonesia, fokus pada desain produk digital dan Figma.
- "Refactoring UI" (buku) oleh Adam Wathan & Steve Schoger — buku terbaik untuk developer/designer yang mau belajar membuat UI yang bagus. Sangat praktis.

Portofolio wajib sebelum melamar:
Minimal 2 case study yang menunjukkan proses lengkap: riset → wireframe → high-fidelity → prototype → evaluasi.

---chunk---
### Metadata
```json
{
  "career_track": "ui_ux_designer",
  "content_type": "salary_context",
  "seniority": "all",
  "language": "en",
  "tags": ["salary", "indonesia", "compensation"]
}
```
### Content
**UI/UX Designer compensation — Indonesian market (2026)**

| Level | Jakarta (IDR/month) | Remote SEA (USD/month) |
|---|---|---|
| Junior (0–2yr) | Rp 4–9 juta | $600–1,200 |
| Mid-level (2–5yr) | Rp 9–20 juta | $1,200–2,800 |
| Senior (5–8yr) | Rp 20–40 juta | $2,800–5,500 |
| Lead/Staff (8yr+) | Rp 40–80 juta | $5,500–12,000 |

Designers at product companies (Gojek, Tokopedia, Traveloka, Shopee) earn significantly above market. Designers who can code (HTML/CSS, Framer) or who have strong quantitative skills (A/B testing, analytics) command a 15–25% premium. Portfolio quality is the single biggest salary differentiator in this field.

---

---

# TRACK: Digital Marketer

---

## 1. Role Definition

---chunk---
### Metadata
```json
{
  "career_track": "digital_marketer",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "en",
  "tags": ["role", "overview", "marketing", "growth", "what-is"]
}
```
### Content
A Digital Marketer drives business growth through digital channels — search engines, social media, email, content, and paid advertising. Unlike traditional marketing, digital marketing is highly measurable: every action, click, and conversion can be tracked, analyzed, and optimized. This data-driven nature has made digital marketing a technical discipline in 2026, requiring marketers who are comfortable with analytics platforms, advertising tools, and increasingly, AI-powered marketing automation.

Day-to-day work varies significantly by specialization but typically involves: managing paid advertising campaigns (Meta Ads, Google Ads), creating and optimizing content for SEO, analyzing performance data, running A/B tests, managing email campaigns, and building marketing automation workflows. Senior digital marketers operate as growth strategists — designing full-funnel acquisition strategies, managing significant budgets, and connecting marketing metrics to business outcomes.

In Indonesia, digital marketing is one of the most accessible career paths and has one of the lowest barriers to entry — but also one of the widest skill gaps between junior and senior levels. The difference between a Rp 5 juta/month social media manager and a Rp 30 juta/month growth lead is fundamentally about whether the person can run data-driven campaigns and prove ROI.

---chunk---
### Metadata
```json
{
  "career_track": "digital_marketer",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "id",
  "tags": ["role", "overview", "marketing", "growth", "what-is"]
}
```
### Content
Digital Marketer mendorong pertumbuhan bisnis melalui saluran digital — mesin pencari, media sosial, email, konten, dan iklan berbayar. Berbeda dengan pemasaran tradisional, pemasaran digital sangat terukur: setiap tindakan, klik, dan konversi dapat dilacak, dianalisis, dan dioptimalkan.

Pekerjaan sehari-hari meliputi: mengelola kampanye iklan berbayar (Meta Ads, Google Ads), membuat dan mengoptimasi konten untuk SEO, menganalisis data performa, menjalankan A/B test, mengelola kampanye email, dan membangun workflow otomasi pemasaran.

Di Indonesia, perbedaan antara social media manager Rp 5 juta/bulan dan growth lead Rp 30 juta/bulan pada dasarnya tentang apakah seseorang bisa menjalankan kampanye berbasis data dan membuktikan ROI.

---

## 2. Skill Taxonomy

---chunk---
### Metadata
```json
{
  "career_track": "digital_marketer",
  "content_type": "skill_taxonomy",
  "seniority": "beginner",
  "language": "en",
  "tags": ["skill-order", "foundations", "beginner"]
}
```
### Content
**Phase 1 — Foundations**

1. **Marketing fundamentals** — The 4Ps, funnel thinking (awareness → consideration → conversion → retention), customer personas, value propositions. The mental models everything else builds on.
2. **Content marketing** — Writing for digital audiences, content calendar planning, copywriting basics, content formats (blog, video, carousel, stories).
3. **Social media marketing** — Platform algorithms (Instagram, TikTok, LinkedIn, X), community management, scheduling tools, engagement metrics.
4. **Google Analytics 4 (GA4)** — Sessions, users, bounce rate, conversion tracking, UTM parameters, funnel analysis. Analytics is the minimum viable skill for any digital marketer.
5. **SEO basics** — Keyword research (Google Keyword Planner, Ubersuggest), on-page optimization, meta tags, search intent, content structure.
6. **Email marketing basics** — List building, segmentation, open rate/CTR, A/B testing subject lines, basic automation (welcome sequences).
7. **Meta Ads basics** — Campaign structure (Campaign → Ad Set → Ad), audience targeting, basic creatives, budget management, reading the Ads Manager.

---chunk---
### Metadata
```json
{
  "career_track": "digital_marketer",
  "content_type": "skill_taxonomy",
  "seniority": "junior",
  "language": "en",
  "tags": ["skill-order", "junior-to-mid"]
}
```
### Content
**Phase 2 — Performance Marketing**

1. **Google Ads** — Search campaigns, Shopping ads, Display network, keyword match types, Quality Score, conversion tracking, bidding strategies.
2. **Advanced Meta Ads** — Pixel setup, custom conversions, lookalike audiences, retargeting funnels, creative testing at scale, ROAS optimization.
3. **TikTok Ads** — Rapidly growing in Indonesian market. Creative-first approach, Spark Ads, performance benchmarks specific to platform.
4. **Advanced SEO** — Technical SEO (site speed, Core Web Vitals, schema markup), link building strategies, content clusters, local SEO.
5. **Marketing analytics deep dive** — Attribution modeling, cohort analysis, LTV calculation, CAC analysis, channel mix modeling.
6. **CRM & marketing automation** — HubSpot or Klaviyo, behavioral triggers, segmentation, drip campaigns, lead scoring.
7. **Landing page optimization** — Heatmaps (Hotjar), A/B testing tools (Google Optimize), conversion rate optimization principles.
8. **Budget management** — Managing 5–50M IDR monthly ad budgets, pacing, forecasting, ROI reporting to stakeholders.

---chunk---
### Metadata
```json
{
  "career_track": "digital_marketer",
  "content_type": "skill_taxonomy",
  "seniority": "mid",
  "language": "en",
  "tags": ["skill-order", "mid-to-senior", "growth", "advanced"]
}
```
### Content
**Phase 3 — Growth Strategy**

1. **Full-funnel growth strategy** — Designing acquisition, activation, retention, referral, and revenue strategies across all channels.
2. **AI-powered marketing** — Using AI for content generation, audience segmentation, predictive analytics, automated bidding, personalization at scale.
3. **Product analytics** — Amplitude or Mixpanel for product-led growth analysis, funnel optimization, feature adoption metrics.
4. **Influencer & creator economy** — KOL (Key Opinion Leader) strategy for Indonesian market, contracts, performance measurement, micro vs macro influencers.
5. **Brand strategy** — Brand positioning, tone of voice, brand guidelines, long-term brand equity vs short-term performance balance.
6. **Marketing team leadership** — Managing junior marketers, agency relationships, budget ownership, executive reporting.

---

## 3. Milestones & Resources

---chunk---
### Metadata
```json
{
  "career_track": "digital_marketer",
  "content_type": "milestone_template",
  "seniority": "beginner",
  "language": "en",
  "tags": ["milestone", "phase-1"]
}
```
### Content
**Milestone: First Live Campaign with Real Results**
Duration: 6–8 weeks
- Run a real Meta Ads campaign (even with a small budget — Rp 500K is enough to learn)
- Set up GA4 with proper event tracking and conversion goals
- Write 5 pieces of SEO-optimized content, track rankings over 4 weeks
- Signal: can show a spreadsheet with campaign spend, impressions, clicks, conversions, CPA — and explain what they mean

**Milestone: Google Analytics Certification + Campaign Case Study**
Duration: 4–6 weeks
- Complete Google Analytics Individual Qualification (free, official)
- Complete Google Ads certification (free, official)
- Document a campaign: before state → strategy → execution → results → learnings
- Signal: can present a campaign performance review to a client or manager and answer data questions confidently

---chunk---
### Metadata
```json
{
  "career_track": "digital_marketer",
  "content_type": "resource",
  "skill_name": "digital marketing",
  "seniority": "beginner",
  "language": "id",
  "tags": ["resource", "digital-marketing", "indonesia"]
}
```
### Content
**Sumber belajar Digital Marketing (Bahasa Indonesia)**

Gratis:
- Google Skillshop (skillshop.google.com) — sertifikasi resmi Google untuk Google Ads, Analytics, dan lainnya. Gratis dan diakui industri.
- Meta Blueprint (facebook.com/business/learn) — kursus resmi Meta untuk Facebook dan Instagram Ads. Gratis.
- YouTube: NGIKLAN channel, Nge-Marketing — konten digital marketing Indonesia yang praktis.

Berbayar:
- Dicoding "Belajar Fundamental Front-End Web" — untuk pemahaman web yang membantu marketer memahami landing page.
- Udemy "The Complete Digital Marketing Course" — komprehensif, mencakup semua channel, sering diskon Rp 100-200rb.

Wajib dimiliki sebelum melamar:
- Google Analytics Certification (GA4)
- Meta Blueprint Certification (minimal Meta Ads)
- Portofolio kampanye nyata, meskipun kecil: tunjukkan angka, bukan hanya gambar kreatif

---chunk---
### Metadata
```json
{
  "career_track": "digital_marketer",
  "content_type": "salary_context",
  "seniority": "all",
  "language": "id",
  "tags": ["salary", "indonesia", "compensation"]
}
```
### Content
**Kompensasi Digital Marketer — Pasar Indonesia (2026)**

| Level | Jakarta (IDR/bulan) | Remote SEA (USD/bulan) |
|---|---|---|
| Junior / Social Media Specialist (0–2thn) | Rp 4–8 juta | $500–1,000 |
| Mid / Performance Marketer (2–5thn) | Rp 8–18 juta | $1,000–2,500 |
| Senior / Growth Lead (5–8thn) | Rp 18–35 juta | $2,500–5,000 |
| Head of Marketing (8thn+) | Rp 35–80 juta | $5,000–12,000 |

Perbedaan kompensasi terbesar ada antara "orang yang bisa bikin konten bagus" dan "orang yang bisa membuktikan ROI dari setiap Rupiah yang dikeluarkan." Marketer yang menguasai data analytics, performance marketing, dan strategi pertumbuhan bisa bernegoisasi gaji 2–3x di atas marketer yang hanya menguasai content creation.

---

---

# TRACK: Cybersecurity Analyst

---

## 1. Role Definition

---chunk---
### Metadata
```json
{
  "career_track": "cybersecurity_analyst",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "en",
  "tags": ["role", "overview", "cybersecurity", "what-is"]
}
```
### Content
A Cybersecurity Analyst protects an organization's systems, networks, and data from cyber threats. The role involves monitoring for suspicious activity, analyzing security incidents, identifying vulnerabilities before attackers do, implementing security controls, and responding to breaches. In 2026, with the proliferation of AI-powered attacks, cloud environments, and Indonesia's growing digital economy, cybersecurity professionals are among the most urgently needed and undersupplied in the country.

Specializations within cybersecurity include: SOC Analyst (Security Operations Center — monitoring and incident response), Penetration Tester / Ethical Hacker (proactively finding vulnerabilities), Security Engineer (building secure systems and infrastructure), Cloud Security Specialist, and Application Security Engineer. Most professionals start as SOC Analysts or in GRC (Governance, Risk, Compliance) before specializing.

Indonesia's Badan Siber dan Sandi Negara (BSSN) and the growth of financial services, e-commerce, and government digital services have created significant institutional demand for cybersecurity talent. The Indonesian cybersecurity talent gap is estimated at tens of thousands of professionals — making this one of the most opportunity-rich tracks for the next decade.

---chunk---
### Metadata
```json
{
  "career_track": "cybersecurity_analyst",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "id",
  "tags": ["role", "overview", "cybersecurity", "what-is"]
}
```
### Content
Cybersecurity Analyst melindungi sistem, jaringan, dan data organisasi dari ancaman siber. Peran ini melibatkan pemantauan aktivitas mencurigakan, analisis insiden keamanan, identifikasi kerentanan sebelum penyerang menemukannya, implementasi kontrol keamanan, dan respons terhadap pelanggaran.

Di Indonesia, kebutuhan profesional keamanan siber sangat mendesak. BSSN (Badan Siber dan Sandi Negara) dan pertumbuhan layanan keuangan digital, e-commerce, dan layanan pemerintah digital menciptakan permintaan institusional yang signifikan. Kesenjangan talent keamanan siber Indonesia diperkirakan mencapai puluhan ribu profesional.

---

## 2. Skill Taxonomy

---chunk---
### Metadata
```json
{
  "career_track": "cybersecurity_analyst",
  "content_type": "skill_taxonomy",
  "seniority": "beginner",
  "language": "en",
  "tags": ["skill-order", "foundations", "beginner", "networking"]
}
```
### Content
**Phase 1 — Foundations**

1. **Networking fundamentals** — TCP/IP, OSI model, DNS, HTTP/HTTPS, FTP, SSH, firewalls, VPNs, subnets, routing. Cannot do security without deeply understanding how networks work.
2. **Linux command line** — File permissions, process management, log files, network commands (netstat, nmap basics), shell scripting. Most security tools run on Linux.
3. **Windows fundamentals** — Active Directory, Group Policy, Registry, Windows Event Logs, PowerShell basics. Most corporate environments run Windows.
4. **Security concepts** — CIA triad (Confidentiality, Integrity, Availability), authentication vs authorization, encryption basics (symmetric vs asymmetric), PKI, TLS/SSL.
5. **Common attack types** — Phishing, SQL injection, XSS, CSRF, man-in-the-middle, ransomware, DDoS. Understanding how attacks work is prerequisite for defense.
6. **Wireshark** — Packet capture and analysis. Understanding what's actually moving on the network.
7. **Python basics** — For writing security scripts, automating scans, parsing logs. Most security automation is Python.
8. **CompTIA Security+ concepts** — Study the Security+ curriculum even if you don't take the exam. It's a comprehensive baseline for security knowledge.

---chunk---
### Metadata
```json
{
  "career_track": "cybersecurity_analyst",
  "content_type": "skill_taxonomy",
  "seniority": "junior",
  "language": "en",
  "tags": ["skill-order", "junior-to-mid", "soc", "penetration-testing"]
}
```
### Content
**Phase 2 — SOC & Offensive Fundamentals**

1. **SIEM tools** — Splunk or Microsoft Sentinel for log aggregation, search, correlation rules, alert creation. The primary tool of SOC analysts.
2. **Incident response process** — Detection → Containment → Eradication → Recovery → Lessons Learned. NIST IR framework.
3. **Vulnerability scanning** — Nessus, OpenVAS, Qualys. Running scans, interpreting results, prioritizing remediation.
4. **Penetration testing basics** — Kali Linux, Metasploit, Nmap, Burp Suite basics. Ethical hacking methodology (reconnaissance → scanning → exploitation → post-exploitation → reporting).
5. **OWASP Top 10** — The 10 most critical web application security risks. Every security professional must know these cold.
6. **Cloud security basics** — AWS/GCP/Azure security services (IAM, Security Groups, Cloud Trail, GuardDuty), shared responsibility model.
7. **Threat intelligence** — MITRE ATT&CK framework, threat actors, TTP analysis, indicators of compromise (IoCs).
8. **Security scripting** — Python scripts for: log parsing, network scanning, automated reporting, API security testing.

---chunk---
### Metadata
```json
{
  "career_track": "cybersecurity_analyst",
  "content_type": "skill_taxonomy",
  "seniority": "mid",
  "language": "en",
  "tags": ["skill-order", "mid-to-senior", "advanced"]
}
```
### Content
**Phase 3 — Advanced Security**

1. **Advanced penetration testing** — Web app pentesting, network pentesting, social engineering, red team operations, writing professional pentest reports.
2. **Malware analysis** — Static analysis (strings, PE headers), dynamic analysis (sandboxing), reverse engineering basics (Ghidra, IDA Pro).
3. **Digital forensics** — Memory forensics, disk forensics, network forensics, chain of custody, forensic tools (Autopsy, Volatility).
4. **DevSecOps** — Integrating security into CI/CD pipelines, SAST/DAST tools, container security scanning, security gates in deployment.
5. **Zero trust architecture** — Identity-centric security, microsegmentation, continuous verification. The modern enterprise security model.
6. **Compliance & regulation** — ISO 27001, SOC 2, Indonesia's UU PDP (Personal Data Protection Law), BSSN guidelines, PCI-DSS for fintech.
7. **Security leadership** — Building security programs, security awareness training, vendor risk management, board-level security reporting.

---

## 3. Milestones & Resources

---chunk---
### Metadata
```json
{
  "career_track": "cybersecurity_analyst",
  "content_type": "milestone_template",
  "seniority": "beginner",
  "language": "en",
  "tags": ["milestone", "phase-1", "ctf", "foundations"]
}
```
### Content
**Milestone: First CTF Completion**
Duration: 6–8 weeks
- Complete 20 TryHackMe rooms (free path available) covering: networking, Linux, web fundamentals, basic exploitation
- Complete at least one Capture The Flag (CTF) challenge — PicoCTF is beginner-friendly
- Set up a home lab: Kali Linux in VirtualBox, one vulnerable VM (Metasploitable)
- Signal: can explain how a SQL injection attack works, demonstrate it on a practice environment, and explain how to prevent it

**Milestone: CompTIA Security+ Certification**
Duration: 8–12 weeks
- This certification is the industry baseline for cybersecurity roles
- It validates: threat analysis, cryptography, network security, identity management, risk management
- Signal: passed the exam. This certification actively opens doors to junior SOC positions in Indonesian banks, telcos, and government.

---chunk---
### Metadata
```json
{
  "career_track": "cybersecurity_analyst",
  "content_type": "resource",
  "skill_name": "cybersecurity",
  "seniority": "beginner",
  "language": "id",
  "tags": ["resource", "cybersecurity", "indonesia", "beginner"]
}
```
### Content
**Sumber belajar Cybersecurity (Bahasa Indonesia & Inggris)**

Platform praktis (sangat direkomendasikan):
- TryHackMe (tryhackme.com) — platform belajar cybersecurity hands-on, browser-based. Ada learning path gratis untuk pemula. Cara belajar terbaik untuk keamanan siber karena langsung praktek.
- Hack The Box (hackthebox.com) — level lebih advanced dari TryHackMe. Untuk yang sudah punya dasar.
- PicoCTF (picoctf.org) — CTF (Capture The Flag) untuk pemula, gratis, dari Carnegie Mellon University.

Bahasa Indonesia:
- Dicoding "Belajar Keamanan Jaringan Komputer" — dasar jaringan dan keamanan, Bahasa Indonesia, bersertifikat.
- YouTube: id-cf channel, Ethical Hacker Indonesia — konten keamanan siber Indonesia.

Sertifikasi yang diakui industri Indonesia (urutan prioritas):
1. CompTIA Security+ — baseline yang diakui hampir semua perusahaan
2. CEH (Certified Ethical Hacker) — diakui di sektor perbankan dan pemerintah Indonesia
3. OSCP (Offensive Security Certified Professional) — untuk penetration tester, sangat dihargai
4. ISO 27001 Lead Implementer — untuk GRC dan compliance roles

---chunk---
### Metadata
```json
{
  "career_track": "cybersecurity_analyst",
  "content_type": "salary_context",
  "seniority": "all",
  "language": "en",
  "tags": ["salary", "indonesia", "compensation"]
}
```
### Content
**Cybersecurity Analyst compensation — Indonesian market (2026)**

| Level | Jakarta (IDR/month) | Remote SEA (USD/month) |
|---|---|---|
| Junior SOC / GRC (0–2yr) | Rp 6–12 juta | $800–1,500 |
| Mid SOC / Pentester (2–5yr) | Rp 12–25 juta | $1,500–3,500 |
| Senior Security Engineer (5–8yr) | Rp 25–55 juta | $3,500–7,000 |
| Security Lead / CISO (8yr+) | Rp 55–120 juta | $7,000–18,000 |

Highest-paying sectors in Indonesia: Banking and financial services (OJK-regulated institutions must have cybersecurity teams), telcos, government agencies (BSSN, BPJS, BPS), and large e-commerce platforms. Penetration testers and red team specialists command premium rates. OSCP certification is a strong salary signal for offensive security roles.

---

---

# TRACK: Data Analyst

---

## 1. Role Definition

---chunk---
### Metadata
```json
{
  "career_track": "data_analyst",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "en",
  "tags": ["role", "overview", "data", "analytics", "what-is"]
}
```
### Content
A Data Analyst transforms raw data into insights that drive business decisions. They collect, clean, analyze, and visualize data — answering questions like "Why did revenue drop last month?", "Which user segment converts best?", or "What's the ROI of this marketing campaign?" The role sits at the intersection of statistics, business understanding, and communication.

Day-to-day work involves: writing SQL queries to extract and transform data, building dashboards in Tableau/Looker/Power BI/Metabase, performing statistical analysis in Python or Excel, creating reports for stakeholders, and collaborating with product managers, marketers, and business leaders to define the right questions to answer.

Data Analyst is one of the most accessible high-paying paths in Indonesian tech. SQL + Excel + basic Python is achievable in 6–9 months and immediately employable. Many successful data analysts come from finance, accounting, and social science backgrounds — analytical thinking and business context transfer well.

---chunk---
### Metadata
```json
{
  "career_track": "data_analyst",
  "content_type": "role_definition",
  "seniority": "all",
  "language": "id",
  "tags": ["role", "overview", "data", "analytics", "what-is"]
}
```
### Content
Data Analyst mengubah data mentah menjadi wawasan yang mendorong keputusan bisnis. Mereka mengumpulkan, membersihkan, menganalisis, dan memvisualisasikan data — menjawab pertanyaan seperti "Mengapa pendapatan turun bulan lalu?", "Segmen pengguna mana yang paling banyak melakukan konversi?", atau "Apa ROI dari kampanye marketing ini?"

Data Analyst adalah salah satu jalur bergaji tinggi yang paling mudah diakses di tech Indonesia. SQL + Excel + Python dasar bisa dicapai dalam 6–9 bulan dan langsung bisa dipekerjakan. Banyak data analyst sukses berasal dari latar belakang keuangan, akuntansi, dan ilmu sosial — pemikiran analitis dan konteks bisnis sangat mudah dialihkan.

---

## 2. Skill Taxonomy

---chunk---
### Metadata
```json
{
  "career_track": "data_analyst",
  "content_type": "skill_taxonomy",
  "seniority": "beginner",
  "language": "en",
  "tags": ["skill-order", "foundations", "beginner"]
}
```
### Content
**Phase 1 — Foundations**

1. **Excel / Google Sheets advanced** — Pivot tables, VLOOKUP/XLOOKUP, INDEX-MATCH, array formulas, conditional formatting, basic charts. Many analysts use Excel daily even at senior levels.
2. **SQL** — SELECT, WHERE, GROUP BY, ORDER BY, JOINs (INNER, LEFT, RIGHT), subqueries, window functions (ROW_NUMBER, RANK, LAG, LEAD), CTEs. SQL is the single most important skill for a data analyst.
3. **Data visualization principles** — Choosing the right chart type, avoiding misleading visuals, color usage, labeling, storytelling with data.
4. **Statistics fundamentals** — Mean, median, mode, standard deviation, distributions, correlation vs causation, basic hypothesis testing, p-values.
5. **Business acumen basics** — Understanding common business metrics: revenue, CAC, LTV, churn rate, MoM growth, conversion rate. Data without business context is noise.
6. **Python basics (Pandas)** — DataFrames, loading CSVs, filtering, groupby, merge, basic plotting with Matplotlib/Seaborn.
7. **One BI tool** — Tableau Public (free), Metabase (open-source), or Power BI Desktop (free). Build dashboards that non-technical stakeholders can understand.

---chunk---
### Metadata
```json
{
  "career_track": "data_analyst",
  "content_type": "skill_taxonomy",
  "seniority": "junior",
  "language": "en",
  "tags": ["skill-order", "junior-to-mid"]
}
```
### Content
**Phase 2 — Mid-level Analytics**

1. **Advanced SQL** — Query optimization, EXPLAIN ANALYZE, indexing strategy for analytical queries, working with semi-structured data (JSON in Postgres), dbt basics.
2. **Python for data analysis** — NumPy, SciPy, advanced Pandas (merge types, apply, transform), time series analysis, statistical testing in Python.
3. **A/B testing & experimentation** — Designing experiments, sample size calculation, statistical significance, avoiding common pitfalls (p-hacking, multiple testing).
4. **Product analytics** — Funnel analysis, cohort retention analysis, user journey mapping with data, event tracking schemas.
5. **dbt (data build tool)** — Transforming raw data into analytics-ready models, testing, documentation. Modern data stack standard.
6. **Data pipeline basics** — Understanding ETL/ELT, Airflow basics, working with data engineers on pipeline design.
7. **Advanced visualization** — Plotly for interactive charts, dashboard design for executive audiences, embedding analytics in products.

---chunk---
### Metadata
```json
{
  "career_track": "data_analyst",
  "content_type": "skill_taxonomy",
  "seniority": "mid",
  "language": "en",
  "tags": ["skill-order", "mid-to-senior", "advanced"]
}
```
### Content
**Phase 3 — Senior Analytics**

1. **Analytics engineering** — Owning the data model layer (dbt), defining metrics consistently across the company, building semantic layers.
2. **Machine learning for analysts** — Using ML models for: customer segmentation (clustering), churn prediction, forecasting, recommendation systems. Not building models from scratch, but understanding and applying them.
3. **Executive communication** — Translating complex analysis into executive summaries, presenting to C-suite, influencing strategy with data.
4. **Causal inference** — Difference-in-differences, regression discontinuity, instrumental variables. Going beyond correlation to understand causation.
5. **Real-time analytics** — Working with streaming data (Kafka basics), real-time dashboards, event-driven analytics architectures.
6. **Data governance** — Data quality frameworks, data dictionaries, PII handling (UU PDP compliance for Indonesian companies), data lineage.

---

## 3. Milestones & Resources

---chunk---
### Metadata
```json
{
  "career_track": "data_analyst",
  "content_type": "milestone_template",
  "seniority": "beginner",
  "language": "en",
  "tags": ["milestone", "phase-1", "portfolio"]
}
```
### Content
**Milestone: SQL Proficiency + First Dashboard**
Duration: 6–8 weeks
- Complete Mode Analytics SQL Tutorial or pgexercises.com up to advanced level
- Write 30 progressively harder SQL queries on a real public dataset (use Google BigQuery public datasets — free)
- Build one complete dashboard in Tableau Public or Metabase: must have 5+ charts, filters, and a clear narrative
- Signal: given a business question ("Which product categories have declining revenue?"), can write the SQL and build the visualization independently in under 2 hours

**Milestone: End-to-End Analytics Project**
Duration: 4–6 weeks
- Choose a public dataset (Kaggle, data.go.id, or BPS data)
- Frame a real business question, clean the data, perform exploratory analysis, build insights, present findings
- Document as a case study (GitHub or Medium): problem → data → analysis → insights → recommendations
- Signal: can show this project in an interview and explain every decision made

---chunk---
### Metadata
```json
{
  "career_track": "data_analyst",
  "content_type": "resource",
  "skill_name": "SQL and analytics",
  "seniority": "beginner",
  "language": "id",
  "tags": ["resource", "sql", "analytics", "indonesia", "beginner"]
}
```
### Content
**Sumber belajar Data Analyst (Bahasa Indonesia & Inggris)**

SQL (prioritas utama):
- pgexercises.com — latihan SQL berbasis PostgreSQL, level progresif, gratis. Terbaik untuk membangun SQL muscle.
- Dicoding "Belajar Fundamental Analisis Data" — SQL + Python + visualisasi, Bahasa Indonesia, bersertifikat. 70 jam, rating 4.83.
- Mode Analytics SQL Tutorial — gratis, pakai data nyata, sangat praktis.

Python untuk analisis:
- Dicoding "Belajar Analisis Data dengan Python" — Pandas, visualisasi, Bahasa Indonesia.
- Kaggle Learn (Python + Pandas) — gratis, interaktif, langsung di browser.

Visualisasi:
- Tableau Public Gallery — pelajari dashboard bagus dari orang lain, kemudian buat sendiri.
- "Storytelling with Data" oleh Cole Nussbaumer Knaflic — buku terbaik tentang komunikasi data visual.

Dataset Indonesia untuk portfolio:
- data.go.id — portal data terbuka pemerintah Indonesia
- BPS (bps.go.id) — Badan Pusat Statistik, data ekonomi dan sosial Indonesia
- Kaggle — dataset global, banyak kompetisi gratis

---chunk---
### Metadata
```json
{
  "career_track": "data_analyst",
  "content_type": "salary_context",
  "seniority": "all",
  "language": "en",
  "tags": ["salary", "indonesia", "compensation"]
}
```
### Content
**Data Analyst compensation — Indonesian market (2026)**

| Level | Jakarta (IDR/month) | Remote SEA (USD/month) |
|---|---|---|
| Junior (0–2yr) | Rp 5–11 juta | $700–1,400 |
| Mid-level (2–5yr) | Rp 11–24 juta | $1,400–3,200 |
| Senior (5–8yr) | Rp 24–50 juta | $3,200–7,000 |
| Analytics Lead / Data Scientist (8yr+) | Rp 50–100 juta | $7,000–15,000 |

Data Analysts with SQL + Python + strong business communication are highly employable across Indonesian industries. Fintech (OVO, GoPay, BRI Finance), e-commerce (Tokopedia, Shopee, Lazada), logistics (Anteraja, SiCepat), and FMCG companies are among the largest employers. Analysts who can do A/B testing and experiment design command a 20–30% premium over pure reporting analysts.

---

---

## Completion Status

| Track | Role Def | Seniority | Skill Taxonomy | Milestones | Resources | Blockers | Salary | Transitions |
|---|---|---|---|---|---|---|---|---|
| Backend Engineer | ✅ EN+ID | ✅ | ✅ 3 phases | ✅ | ✅ EN+ID | ✅ EN+ID | ✅ EN+ID | ✅ |
| Frontend Engineer | ✅ EN+ID | ✅ | ✅ 3 phases | ✅ | ✅ EN+ID | ✅ EN+ID | ✅ EN | ✅ |
| DevOps Engineer | ✅ EN+ID | — | ✅ 3 phases | ✅ | ✅ EN | ✅ EN | ✅ ID | — |
| ML/AI Engineer | ✅ EN+ID | — | ✅ 3 phases | ✅ | ✅ ID | — | ✅ EN | — |
| UI/UX Designer | ✅ EN+ID | — | ✅ 3 phases | ✅ | ✅ ID | — | ✅ EN | ✅ |
| Digital Marketer | ✅ EN+ID | — | ✅ 3 phases | ✅ | ✅ ID | — | ✅ ID | — |
| Cybersecurity Analyst | ✅ EN+ID | — | ✅ 3 phases | ✅ | ✅ ID | — | ✅ EN | — |
| Data Analyst | ✅ EN+ID | — | ✅ 3 phases | ✅ | ✅ ID | — | ✅ EN | — |

**Estimated total chunks across all 8 tracks:** ~380–420 chunks (EN + ID pairs)  
**Estimated one-time embedding cost:** < $1.50 at text-embedding-3-small pricing

> Tracks marked `—` for seniority, blocker, or transition columns have the content functionally covered within the skill taxonomy and role definition chunks. These can be expanded in v2 content iterations based on user query patterns.
