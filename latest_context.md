AI LMS PROJECT — CONTEXT & STATUS (HANDOFF DOCUMENT)
1. PROJECT OVERVIEW

This project is an AI-powered Learning Management System (LMS) designed for schools, not generic online courses.
It supports students, teachers, parents, and admins, with a strong focus on:

Class-based structure (real school model)

AI-assisted tests, notes, and learning tools

Gamified XP system (with anti-abuse controls)

Offline + online model usage (Phi-3 offline, heavier models server-side)

Privacy-preserving student data handling

Backend: FastAPI (Python)
Frontend: React / Next.js (Lovable.dev-generated UI)
Database: PostgreSQL
AI models: Local via Ollama + server-side models later

2. CORE DOMAIN MODEL (LOCKED)
2.1 Users

Student

Teacher

Parent

Admin / Super User

2.2 Class-based system (VERY IMPORTANT)

This LMS follows real school structure:

Students belong to exactly one class

Class is derived automatically from a 6-digit registration code

First 2 digits → Grade (09–12)

Next 2 digits → Section (A=01, B=02, C=03)

Last 2 digits → Roll number

Teachers are NOT directly assigned to classes

Teachers are assigned to subjects

Subjects are assigned to classes

Therefore, the linkage is:

Teacher → Subject → Class → Students


This is intentional and correct.

3. SUBJECT SYSTEM (PHASE 2 COMPLETE)
3.1 Subject Types

Core subjects

Belong to exactly one class

Exactly one teacher per subject

Students are auto-enrolled

Elective subjects

Extra-curricular subjects

Students enroll manually (future)

Teachers assigned by admin

Can span across classes

3.2 Admin-only Control

Only admins/super users can create subjects

Teachers and students cannot create or modify subjects

4. PHASE STATUS SUMMARY
✅ Phase 1 — Auth & Basic Setup

Signup & login pages exist

Password hashing uses Argon2 (bcrypt removed due to conflicts)

No JWT yet (DEV mode auth)

/auth/login returns:

user_id

role

class_id

No bearer token yet (this is expected)

✅ Phase 2.1 — Subjects Introduced

subjects table exists

subject_students table exists

✅ Phase 2.2 — Admin-only Subject Creation + Auto Enrollment

Core subjects:

Admin creates subject

Students in class auto-enrolled

Teacher assigned via subject

✅ Phase 2.3 — Teacher Dashboard Scoping

Teachers can only see students:

In their subject

In their class (for core subjects)

Verified via /teacher/students

✅ Phase 2.4 — Backend Provisioning for Electives (NO UI)

Backend supports (but does not yet expose):

Capacity-limited subjects

Enrollment open/close windows

First-come-first-serve logic

Guard logic exists, but not activated

5. AUTH & SWAGGER STATUS (IMPORTANT)

OAuth2/Bearer added only to Swagger OpenAPI

Purpose: show Authorize button in /docs

Runtime auth is still DEV-mode

get_current_user() does NOT read JWTs

Role checks work based on returned role

/auth/login does NOT return bearer tokens

This is expected

JWT implementation is postponed

6. WORKING CYCLE (WC) STATUS
WC-1 — Data Setup & Linkage Verification ✅ / IN PROGRESS

Goal:

Teacher and student linked via class + subject

Steps:

Class exists (created via student signup)

Student exists and is linked to class

Teacher exists

Admin creates core subject

Subject links teacher to class

Students auto-enrolled

Teacher sees students via /teacher/students

Current blocker resolved:

Teacher not linked because no core subject existed

Fix: Admin must create at least one core subject

WC-1 is expected to be completed next.

WC-2 — Student Test Flow (PLANNED, NOT STARTED)

Goal:

Student generates AI test

Student attempts test

Marks calculated

Teacher sees marks

XP intentionally ignored for now

WC-3 — Student Notes Flow (PLANNED)

Requirements:

AI-generated notes

High quality, textbook-level

KaTeX-rendered math

Stored as:

Raw markdown

Rendered PDF

Student-only content

Teacher sees only:

XP

Timestamp

Student can:

View in-app

Save privately

Download

Regenerate

Discard

7. XP SYSTEM — PAUSED BY DESIGN

XP system is intentionally paused before WC-2/WC-3 to avoid abuse.

Planned XP Principles:

XP is event-based, not action-based

Cooldowns per event (notes, tests, etc.)

One-time XP per meaningful action

Quality gates (e.g., test score thresholds)

Daily / weekly XP caps

Subject-level caps

Full auditability via future xp_events table

No XP wiring should proceed until restrictions are finalized.

8. FRONTEND STATUS (IMPORTANT CONSTRAINTS)

Frontend was generated via Lovable.dev

UI/UX must NOT be altered visually

All future changes must:

Be invisible additions

Preserve existing layout, buttons, XP badges, modals

NotesPage.tsx must:

Retain Generate Notes modal

Retain XP display

Retain search and history components

9. MODELS & AI SETUP

Offline model planned: Phi-3

Heavier models:

Prototype: laptop-friendly

Production: server-hosted

Ollama is installed and working

Models installed via Ollama

Backend will call local models (no cloud dependency for core flows)

10. WHAT IS PENDING (NEXT STEPS)
Immediate Next Steps

Finish WC-1 (create core subject as admin)

Confirm teacher sees student

Proceed to WC-2 (student test flow, no XP)

Only after WC-2 → resume XP system design

Future Phases

WC-3: Notes with KaTeX + PDF

Phase 3: Elective enrollment UI (temporary page)

Phase 4: Admin dashboard

Phase 5: Parent dashboard

Phase 6: Security hardening (JWT, 2FA, device binding)

11. IMPORTANT DEVELOPMENT PRINCIPLES (DO NOT VIOLATE)

Do NOT hallucinate files or routes

Do NOT redesign UI

Do NOT assume JWT exists yet

Do NOT award XP without restrictions

Always follow:

Teacher → Subject → Class → Student

✅ What has been developed so far
1️⃣ Authentication & Security

JWT-based authentication

Role-based route guards (student / teacher)

Token rehydration on frontend

Protected routes in React

Audit logging groundwork added

2️⃣ Tests System (End-to-End)

AI-assisted test generation

Tests stored in DB with questions as structured data

Student test attempt flow:

View available tests

Start test

Answer questions

Submit test

See results (score, percentage, correctness)

Attempts stored with:

raw score

percentage (authoritative, persisted)

Anti-farming logic: XP only on submission

3️⃣ XP System (Backend-Authoritative)

Central XP service (apply_xp_event)

XP rules defined per event

Cooldowns per feature (server-side, cannot be bypassed):

Notes generation

Flashcards

AI chat

Daily streak

Test XP handled separately and based on percentage

XP stored in Progress table:

total XP

level

per-event timestamps (JSON stats)

Level calculated from XP (simple curve, extensible)

4️⃣ Analytics System (Major Focus)

A dedicated analytics layer, not mixed with business logic.

Backend

Central analytics service

Analytics based on both score and percentage

Single main endpoint:

GET /analytics/overview

Student view → own performance

Teacher view → class + subjects

Additional endpoint:

GET /analytics/students

Per-student drill-down

Attempts, avg score, avg percentage

CSV export:

GET /analytics/export/students.csv

Frontend

TeacherDashboard

High-level snapshot

Class average score & percentage

Student count

AnalyticsPage

Detailed analytics

Subject-wise performance

Student table (attendance vs performance)

CSV export button

Clear separation:

Dashboard = summary

Analytics page = explanation

5️⃣ UX / Frontend State

Tests page flicker issues fixed

Routing issues fixed (/teacher/analytics)

Results page fixed:

Back navigation works

Correct / incorrect answers shown

Percentage calculation corrected

Cooldown UI exists for test generation (UI-only for now)

🏗️ Architectural principles locked in

These were explicit decisions, not accidents:

Backend is authoritative (XP, percentage, analytics)

Frontend never recomputes scores

No XP farming

Analytics is read-only and isolated

One analytics contract, many dashboards

JSON fields used for extensibility (stats, questions)

Minimal schema churn, migration-safe changes

🚧 What is NOT done yet (intentionally)

XP leaderboards

Level-up rewards

Parent dashboards

Difficulty-adaptive testing

Time-based analytics / trends

Charts beyond basic bar charts

Admin controls

All of these are natural extensions, not reworks.