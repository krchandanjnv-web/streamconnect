# 💬 StreamConnect — Streamlit Chat App

A real-time chat application built with **Streamlit** + **Google Sheets** as the database backend. Supports user authentication, a friendship system, and a live chat interface — all in a single `app.py`.

---

## 📸 Features

| Feature | Details |
|---|---|
| 🔐 Auth | Login & Signup with SHA-256 hashed passwords |
| 🔑 Password Rule | **Minimum 10 characters** (strictly enforced) |
| 👥 Friendships | Search users → Send request → Accept → Chat |
| 💬 Chat | `st.chat_message` per conversation, filtered per pair |
| 🔄 Pseudo Real-Time | `@st.cache_data(ttl=2)` + Refresh button |
| 🎨 Design | Dark glassmorphism UI with gradient accents |

---

## 🗂️ Google Sheets Structure

Create a Google Sheet with **three worksheets** (tabs) named exactly:

### 1. `users`
| Column | Type | Notes |
|---|---|---|
| `username` | string | Unique username |
| `password_hash` | string | SHA-256 hash of password |

### 2. `requests`
| Column | Type | Notes |
|---|---|---|
| `from_user` | string | Sender of the friend request |
| `to_user` | string | Recipient |
| `status` | string | `pending` or `accepted` |

### 3. `messages`
| Column | Type | Notes |
|---|---|---|
| `sender` | string | Who sent the message |
| `receiver` | string | Who receives it |
| `content` | string | The message text |
| `timestamp` | string | UTC `YYYY-MM-DD HH:MM:SS` |

> **Tip:** Add the header row to each sheet manually before the first run. The app reads with `usecols=` so column names must match exactly.

---

## ⚙️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/streamconnect.git
cd streamconnect

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure secrets
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
# Edit secrets.toml with your Google credentials (see below)

# 5. Run the app
streamlit run app.py
```

---

## 🔑 Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project (or select an existing one).
3. Enable the **Google Sheets API** and **Google Drive API**.
4. Go to **IAM & Admin → Service Accounts → Create Service Account**.
5. Download the JSON key file.
6. Open your Google Sheet → **Share** → paste the `client_email` from the JSON → give **Editor** access.
7. Fill in `.streamlit/secrets.toml` with values from the JSON key.

---

## 🚀 Vercel Deployment

> **Note:** Vercel is primarily for Node.js/serverless. For Streamlit, **Streamlit Community Cloud** is the easiest path, but Vercel works with the config below.

### Option A — Streamlit Community Cloud (Recommended)
1. Push your repo to GitHub (**without** `secrets.toml` — add it to `.gitignore`).
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app → select your repo.
3. Under **Advanced Settings → Secrets**, paste the contents of your `secrets.toml`.
4. Deploy!

### Option B — Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the project root and follow prompts.
3. In the **Vercel Dashboard → Settings → Environment Variables**, add:
   - Key: `STREAMLIT_SECRETS` (or use the `connections.gsheets` format as per [st-gsheets-connection docs](https://github.com/streamlit/gsheets-connection))
   - Paste your full JSON service account content.
4. Re-deploy: `vercel --prod`

---

## 🏗️ Architecture

```
app.py
│
├── init_session()          — Boot session state defaults
├── Data Layer
│   ├── fetch_users()       — @cache_data(ttl=2)
│   ├── fetch_requests()    — @cache_data(ttl=2)
│   ├── fetch_messages()    — @cache_data(ttl=2)
│   ├── add_user()
│   ├── send_friend_request()
│   ├── accept_friend_request()
│   └── send_message()
├── Auth Pages
│   ├── page_login()
│   └── page_signup()       ← 10-char password enforced here
├── App Pages
│   ├── sidebar_nav()
│   ├── page_chat()         ← Filtered per (sender, receiver) pair
│   ├── page_search_users()
│   └── page_friend_requests()
└── main()                  ← Clean entrypoint
```

---

## 🔒 Security Notes

- Passwords are **SHA-256 hashed** before storage — never stored in plain text.
- For production, upgrade to **bcrypt** (`pip install bcrypt`).
- Keep `secrets.toml` out of version control (already in `.gitignore` template).
- Consider adding rate limiting for login attempts in high-traffic deployments.

---

## 📦 Dependencies

```
streamlit>=1.35.0
streamlit-gsheets-connection>=0.0.5
pandas>=2.0.0
gspread>=5.12.0
google-auth>=2.28.0
google-auth-oauthlib>=1.2.0
```

---

## 🎨 UI Design

- **Theme:** Dark glassmorphism with purple/blue gradient accents
- **Font:** DM Sans (body) + DM Mono — loaded from Google Fonts
- **Colors:** `#7c3aed` (violet) · `#4f46e5` (indigo) · `#60a5fa` (blue)
- **Effects:** Backdrop blur cards, gradient text, smooth button transitions

---

## 📄 License

MIT — feel free to fork and build on it!
