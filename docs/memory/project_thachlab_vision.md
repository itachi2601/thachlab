---
name: project-thachlab-vision
description: ThachLab product vision — personal brand site evolving into an LMS for offline students
metadata: 
  node_type: memory
  type: project
  originSessionId: aeb6fa12-c91e-4887-bd44-21b55ca287ba
---

ThachLab is thầy Thạch's (Thach Ngo, itachi2601 on GitHub) personal-brand teaching site. Brand identity: "Teaching Mechanical Engineering & Physics · Living between equation and motion · Gym/Ice skating/Balance" — core message: sống khỏe mạnh, có đam mê, không ngừng học hỏi. Site's job: attract physics students and support his offline classes. Cover banner motto: "Passionate Teaching Can Inspire Students". Socials: facebook.com/ngodieuthach (3.3K followers), Instagram/TikTok: ngo_dieu_thach. He teaches KHTN 9 + THPT physics, studied at THPT Trưng Vương Q.1, lives in HCMC, from Đà Nẵng.

**Roadmap agreed 2026-07-06** (user chose: brand first, then LMS):
1. Phase 1 — brand messaging across homepage/about/footer (in progress).
2. Phase 2 — LMS: student accounts, rewatch lectures (videos already on YouTube — embed, don't host), tests + homework after offline classes, two-way progress tracking (student sees own progress, teacher sees all), alerts when a student's performance declines. Target scale: 500+ students with ambition to expand to mass online courses — plan a real backend (e.g., Supabase; free tier OK to start but design for growth). Static-export hosting stays for the public site; LMS data goes through the backend service client-side or a separate app.

**How to apply:** When adding features, keep the brand voice (physics-in-real-life, health/passion/discipline) and remember the site must keep working on static LiteSpeed hosting ([[project-thachlab-hosting]]) until a hosting change is deliberately made.
