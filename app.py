"""
StreamConnect — Streamlit Chat App backed by Google Sheets.
Version : 2.0.0  (Minimal & Professional — WhatsApp/Messenger style)
"""

import streamlit as st
import pandas as pd
import hashlib
import time
from datetime import datetime, timezone
from streamlit_gsheets import GSheetsConnection

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StreamConnect",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM — Minimal & Professional
# ─────────────────────────────────────────────────────────────────────────────
STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #f0f2f5 !important; }

#MainMenu, footer { visibility: hidden !important; }
.block-container { padding: 1rem 2rem 2rem 2rem !important; max-width: 100% !important; }

/* ── Auth ── */
.auth-outer {
    padding: 3rem 1rem;
}
.auth-card {
    background: #fff; border-radius: 16px;
    padding: 2.5rem 2rem; width: 100%; max-width: 420px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.08);
}
.auth-logo { text-align: center; margin-bottom: 1.75rem; }
.auth-logo-icon { font-size: 2.8rem; display: block; margin-bottom: 0.4rem; }
.auth-logo-title { font-size: 1.5rem; font-weight: 700; color: #1a1a2e; }
.auth-logo-sub   { font-size: 0.85rem; color: #65676b; margin-top: 0.2rem; }

/* ── Inputs ── */
.stTextInput > div > div > input,
.stPasswordInput > div > div > input {
    background: #f0f2f5 !important;
    border: 1.5px solid #e4e6ea !important;
    border-radius: 10px !important;
    color: #1a1a2e !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 0.9rem !important;
    transition: border 0.15s !important;
}
.stTextInput > div > div > input:focus,
.stPasswordInput > div > div > input:focus {
    border-color: #1877f2 !important;
    background: #fff !important;
    box-shadow: 0 0 0 3px rgba(24,119,242,0.1) !important;
}
label { color: #444 !important; font-size: 0.82rem !important; font-weight: 500 !important; }

/* ── Buttons ── */
.stButton > button {
    background: #1877f2 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.5rem !important;
    transition: background 0.15s, transform 0.1s !important;
    width: 100%;
}
.stButton > button:hover { background: #166fe5 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Contact rows ── */
.contact-row {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 0.75rem 0.5rem;
    border-bottom: 1px solid #f7f7f7;
    border-radius: 8px;
    transition: background 0.12s;
}
.contact-row.active { background: #e7f3ff; }
.av {
    width: 42px; height: 42px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 1rem; color: #fff;
    flex-shrink: 0; position: relative;
}
.av-sm {
    width: 30px; height: 30px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.78rem; color: #fff; flex-shrink: 0;
}
.online-dot {
    position: absolute; bottom: 1px; right: 1px;
    width: 11px; height: 11px; border-radius: 50%;
    background: #31a24c; border: 2px solid #fff;
}
.contact-name   { font-size: 0.9rem; font-weight: 600; color: #1a1a2e; }
.contact-status { font-size: 0.75rem; color: #65676b; margin-top: 1px; }

/* ── Bubble messages ── */
.msg-wrap { display: flex; margin-bottom: 0.5rem; align-items: flex-end; gap: 0.4rem; }
.msg-wrap.me { flex-direction: row-reverse; }
.bubble {
    max-width: 68%; padding: 0.55rem 0.85rem;
    border-radius: 18px; font-size: 0.88rem; line-height: 1.5;
    word-wrap: break-word; box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
.bubble.them { background: #fff;      color: #1a1a2e; border-bottom-left-radius: 4px; }
.bubble.me   { background: #dcf8c6;   color: #1a1a2e; border-bottom-right-radius: 4px; }
.bubble-del  { background: #f0f0f0 !important; color: #999 !important; font-style: italic; }
.bubble-meta {
    font-size: 0.68rem; color: #aaa; margin-top: 0.2rem;
    display: flex; align-items: center; justify-content: flex-end; gap: 3px;
}
.read-tick { color: #53bdeb; }
.date-div {
    text-align: center; margin: 0.75rem 0; font-size: 0.72rem; color: #65676b;
}
.date-div span { background: #e1d7c9; padding: 0.2rem 0.75rem; border-radius: 10px; }

/* ── Search / Request cards ── */
.sc-card {
    background: #fff; border-radius: 12px; padding: 1rem 1.25rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07); margin-bottom: 0.75rem;
    display: flex; align-items: center; gap: 1rem;
}
.sc-card-name { font-size: 0.95rem; font-weight: 600; color: #1a1a2e; }
.sc-card-sub  { font-size: 0.78rem; color: #65676b; margin-top: 2px; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: #f0f2f5 !important; border-radius: 10px !important; }
.stTabs [data-baseweb="tab"]      { color: #65676b !important; font-weight: 500 !important; }
.stTabs [aria-selected="true"]    { color: #1877f2 !important; background: #e7f3ff !important; border-radius: 8px !important; }

/* ── Chat input ── */
[data-testid="stChatInputTextArea"] {
    background: #fff !important; border: 1px solid #e4e6ea !important;
    border-radius: 24px !important; color: #1a1a2e !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Delete btn ── */
.del-btn > button {
    background: transparent !important; color: #ccc !important;
    border: none !important; width: auto !important;
    padding: 0.1rem 0.35rem !important; font-size: 0.75rem !important;
    border-radius: 6px !important;
}
.del-btn > button:hover { background: #ffe4e4 !important; color: #d32f2f !important; }

hr { border-color: #e4e6ea !important; }
.stAlert { border-radius: 10px !important; }
</style>
"""

# ── Avatar palette ──
AVATAR_COLORS = ["#1877f2","#e91e63","#9c27b0","#ff5722","#009688","#ff9800","#3f51b5","#00bcd4"]

def av_color(name):
    return AVATAR_COLORS[sum(ord(c) for c in name) % len(AVATAR_COLORS)]

def av_letter(name):
    return name[0].upper() if name else "?"

def avatar_html(name, cls="av", online=False):
    dot = '<span class="online-dot"></span>' if online else ""
    return f'<div class="{cls}" style="background:{av_color(name)};">{av_letter(name)}{dot}</div>'

def now_ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

def fmt_time(ts_str):
    try:
        dt = datetime.strptime(str(ts_str), "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%I:%M %p").lstrip("0")
    except Exception:
        return ""

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


# ─────────────────────────────────────────────────────────────────────────────
# DATA LAYER
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=2)
def fetch_users(_conn):
    try:
        df = _conn.read(worksheet="users", usecols=["username","password_hash"], ttl=2)
        return df.dropna(subset=["username"])
    except Exception:
        return pd.DataFrame(columns=["username","password_hash"])

@st.cache_data(ttl=2)
def fetch_requests(_conn):
    try:
        df = _conn.read(worksheet="requests", usecols=["from_user","to_user","status"], ttl=2)
        return df.dropna(subset=["from_user","to_user"])
    except Exception:
        return pd.DataFrame(columns=["from_user","to_user","status"])

@st.cache_data(ttl=2)
def fetch_messages(_conn):
    try:
        df = _conn.read(worksheet="messages",
                        usecols=["sender","receiver","content","timestamp","read","deleted"], ttl=2)
        return df.dropna(subset=["sender","receiver","content"])
    except Exception:
        return pd.DataFrame(columns=["sender","receiver","content","timestamp","read","deleted"])

@st.cache_data(ttl=5)
def fetch_online(_conn):
    try:
        df = _conn.read(worksheet="online", usecols=["username","last_seen"], ttl=5)
        return df.dropna(subset=["username"])
    except Exception:
        return pd.DataFrame(columns=["username","last_seen"])

def add_user(conn, username, pw_hash):
    df = fetch_users(conn)
    df = pd.concat([df, pd.DataFrame([{"username":username,"password_hash":pw_hash}])], ignore_index=True)
    conn.update(worksheet="users", data=df); fetch_users.clear()

def send_friend_request(conn, from_user, to_user):
    df = fetch_requests(conn)
    df = pd.concat([df, pd.DataFrame([{"from_user":from_user,"to_user":to_user,"status":"pending"}])], ignore_index=True)
    conn.update(worksheet="requests", data=df); fetch_requests.clear()

def accept_friend_request(conn, from_user, to_user):
    df = fetch_requests(conn)
    df.loc[(df["from_user"]==from_user)&(df["to_user"]==to_user), "status"] = "accepted"
    conn.update(worksheet="requests", data=df); fetch_requests.clear()

def send_message(conn, sender, receiver, content):
    df = fetch_messages(conn)
    df = pd.concat([df, pd.DataFrame([{
        "sender":sender,"receiver":receiver,"content":content,
        "timestamp":now_ts(),"read":"no","deleted":"no"
    }])], ignore_index=True)
    conn.update(worksheet="messages", data=df); fetch_messages.clear()

def mark_read(conn, sender, receiver):
    df = fetch_messages(conn)
    if df.empty: return
    mask = (df["sender"]==sender)&(df["receiver"]==receiver)&(df["read"]!="yes")
    if mask.any():
        df.loc[mask,"read"] = "yes"
        conn.update(worksheet="messages", data=df); fetch_messages.clear()

def delete_message(conn, sender, receiver, timestamp):
    df = fetch_messages(conn)
    mask = (df["sender"]==sender)&(df["receiver"]==receiver)&(df["timestamp"]==timestamp)
    df.loc[mask,"deleted"] = "yes"
    df.loc[mask,"content"] = "🚫 This message was deleted"
    conn.update(worksheet="messages", data=df); fetch_messages.clear()

def update_online(conn, username):
    df = fetch_online(conn)
    ts = now_ts()
    if not df.empty and username in df["username"].values:
        df.loc[df["username"]==username,"last_seen"] = ts
    else:
        df = pd.concat([df, pd.DataFrame([{"username":username,"last_seen":ts}])], ignore_index=True)
    conn.update(worksheet="online", data=df); fetch_online.clear()

def is_online(online_df, username):
    if online_df.empty or username not in online_df["username"].values: return False
    try:
        dt = datetime.strptime(str(online_df[online_df["username"]==username].iloc[0]["last_seen"]),"%Y-%m-%d %H:%M:%S")
        return (datetime.utcnow()-dt).total_seconds() < 30
    except Exception:
        return False


# ─────────────────────────────────────────────────────────────────────────────
# SESSION
# ─────────────────────────────────────────────────────────────────────────────
def init_session():
    for k,v in {"authenticated":False,"username":None,"auth_page":"login","active_contact":None,"nav":"chat"}.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────────────────────────────────────
def page_login(conn):
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<div class="auth-logo"><span class="auth-logo-icon">💬</span>'
                    '<div class="auth-logo-title">StreamConnect</div>'
                    '<div class="auth-logo-sub">Sign in to continue</div></div>', unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="your_username", key="li_u")
        password = st.text_input("Password", type="password", placeholder="••••••••••", key="li_p")
        if st.button("Sign In"):
            if not username or not password:
                st.error("Please fill in both fields.")
            else:
                users = fetch_users(conn)
                match = users[users["username"]==username.strip()]
                if match.empty or match.iloc[0]["password_hash"] != hash_password(password):
                    st.error("Invalid username or password.")
                else:
                    st.session_state.authenticated = True
                    st.session_state.username = username.strip()
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#65676b;font-size:0.85rem;'>Don't have an account?</p>", unsafe_allow_html=True)
        if st.button("Create Account"):
            st.session_state.auth_page = "signup"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def page_signup(conn):
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<div class="auth-logo"><span class="auth-logo-icon">✨</span>'
                    '<div class="auth-logo-title">Create Account</div>'
                    '<div class="auth-logo-sub">Join StreamConnect today</div></div>', unsafe_allow_html=True)
        username = st.text_input("Choose a username", placeholder="cooluser42", key="su_u")
        password = st.text_input("Password", type="password", placeholder="Min. 10 characters", key="su_p")
        confirm  = st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="su_c")
        if st.button("Create Account"):
            username = username.strip()
            if not username or not password or not confirm:
                st.error("All fields are required.")
            elif len(password) < 10:
                st.error("❌ Password must be at least 10 characters long.")
                st.stop()
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                users = fetch_users(conn)
                if not users.empty and username in users["username"].values:
                    st.error("Username already taken.")
                else:
                    add_user(conn, username, hash_password(password))
                    st.success("Account created! Please sign in.")
                    st.session_state.auth_page = "login"
                    time.sleep(1); st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Sign In"):
            st.session_state.auth_page = "login"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TOP NAV
# ─────────────────────────────────────────────────────────────────────────────
def top_nav(conn):
    me = st.session_state.username
    requests_df = fetch_requests(conn)
    pending = 0
    if not requests_df.empty:
        pending = len(requests_df[(requests_df["to_user"]==me)&(requests_df["status"]=="pending")])

    nav = st.session_state.nav
    st.markdown(
        f"""<div style="background:#fff;border-bottom:1px solid #e4e6ea;padding:0.6rem 1rem;
        margin-bottom:0.75rem;border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,0.06);
        display:flex;align-items:center;gap:0.5rem;">
        <span style="font-size:1.1rem;font-weight:700;color:#1a1a2e;margin-right:1rem;">💬 StreamConnect</span>
        <span style="flex:1;"></span>
        {avatar_html(me,"av-sm")}
        <span style="font-size:0.85rem;font-weight:600;color:#1a1a2e;">{me}</span>
        </div>""",
        unsafe_allow_html=True,
    )

    nav_c1, nav_c2, nav_c3, nav_c4, _, signout_c = st.columns([2,1,1,1,2,1])
    with nav_c2:
        label = "💬 Chats"
        if st.button(label, key="nb_chat", use_container_width=True):
            st.session_state.nav = "chat"; st.rerun()
    with nav_c3:
        if st.button("🔍 Search", key="nb_search", use_container_width=True):
            st.session_state.nav = "search"; st.rerun()
    with nav_c4:
        req_label = f"👥 Requests {'🔴' if pending else ''}"
        if st.button(req_label, key="nb_req", use_container_width=True):
            st.session_state.nav = "request"; st.rerun()
    with signout_c:
        if st.button("🚪 Sign Out", key="nb_signout", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# CHAT PAGE
# ─────────────────────────────────────────────────────────────────────────────
def page_chat(conn):
    me = st.session_state.username
    update_online(conn, me)
    online_df   = fetch_online(conn)
    requests_df = fetch_requests(conn)

    friends = []
    if not requests_df.empty:
        acc = requests_df[requests_df["status"]=="accepted"]
        friends = list(set(
            acc[acc["from_user"]==me]["to_user"].tolist() +
            acc[acc["to_user"]==me]["from_user"].tolist()
        ))

    left, right = st.columns([1, 3], gap="medium")

    # ── Contact panel ──
    with left:
        st.markdown(
            '<div style="background:#fff;border-radius:12px;padding:1rem;'
            'box-shadow:0 1px 4px rgba(0,0,0,0.07);">',
            unsafe_allow_html=True,
        )
        st.markdown('<div style="font-size:1rem;font-weight:700;color:#1a1a2e;margin-bottom:0.75rem;">Contacts</div>', unsafe_allow_html=True)

        if not friends:
            st.markdown('<p style="color:#65676b;font-size:0.85rem;">No contacts yet.<br>Use Search to add friends.</p>', unsafe_allow_html=True)
        else:
            for friend in sorted(friends):
                online = is_online(online_df, friend)
                active = st.session_state.active_contact == friend
                bg = "#e7f3ff" if active else "transparent"
                status_txt = "🟢 Online" if online else "⚪ Offline"
                st.markdown(
                    f'<div class="contact-row {"active" if active else ""}" style="background:{bg};">'
                    f'{avatar_html(friend,"av",online)}'
                    f'<div><div class="contact-name">{friend}</div>'
                    f'<div class="contact-status">{status_txt}</div></div></div>',
                    unsafe_allow_html=True,
                )
                if st.button(f"Open {friend}", key=f"sel_{friend}", use_container_width=True):
                    st.session_state.active_contact = friend
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", use_container_width=True, key="ref_btn"):
            fetch_messages.clear(); fetch_requests.clear(); fetch_online.clear()
            st.rerun()

    # ── Chat panel ──
    with right:
        contact = st.session_state.active_contact

        if not contact:
            st.markdown(
                '<div style="display:flex;flex-direction:column;align-items:center;'
                'justify-content:center;min-height:60vh;color:#aaa;gap:0.75rem;">'
                '<div style="font-size:4rem;">💬</div>'
                '<div style="font-size:1rem;font-weight:500;color:#888;">Select a contact to start chatting</div>'
                '<div style="font-size:0.85rem;color:#bbb;">Your messages will appear here</div></div>',
                unsafe_allow_html=True,
            )
            return

        mark_read(conn, contact, me)
        online = is_online(online_df, contact)

        # Header
        st.markdown(
            f'<div style="background:#fff;border-radius:12px 12px 0 0;padding:0.75rem 1rem;'
            f'border-bottom:1px solid #e4e6ea;display:flex;align-items:center;gap:0.75rem;'
            f'box-shadow:0 1px 3px rgba(0,0,0,0.06);">'
            f'{avatar_html(contact,"av",online)}'
            f'<div><div style="font-size:1rem;font-weight:700;color:#1a1a2e;">{contact}</div>'
            f'<div style="font-size:0.75rem;color:{"#31a24c" if online else "#65676b"};">'
            f'{"🟢 Online now" if online else "⚪ Offline"}</div></div></div>',
            unsafe_allow_html=True,
        )

        # Messages area
        messages_df = fetch_messages(conn)
        if not messages_df.empty:
            convo = messages_df[
                ((messages_df["sender"]==me)      & (messages_df["receiver"]==contact)) |
                ((messages_df["sender"]==contact)  & (messages_df["receiver"]==me))
            ].sort_values("timestamp", ascending=True)
        else:
            convo = pd.DataFrame(columns=["sender","receiver","content","timestamp","read","deleted"])

        chat_box = st.container()
        with chat_box:
            if convo.empty:
                st.markdown(
                    '<p style="text-align:center;color:#aaa;padding:2rem;font-size:0.9rem;">'
                    'No messages yet. Say hello! 👋</p>',
                    unsafe_allow_html=True,
                )
            else:
                last_date = None
                for idx, row in convo.iterrows():
                    is_me      = row["sender"] == me
                    is_deleted = str(row.get("deleted","no")).lower() == "yes"
                    content    = row["content"]
                    time_str   = fmt_time(row.get("timestamp",""))
                    is_read    = str(row.get("read","no")).lower() == "yes"

                    # Date divider
                    try:
                        msg_date = str(row["timestamp"])[:10]
                        if msg_date != last_date:
                            st.markdown(f'<div class="date-div"><span>{msg_date}</span></div>', unsafe_allow_html=True)
                            last_date = msg_date
                    except Exception:
                        pass

                    tick = ""
                    if is_me:
                        tick = '<span class="read-tick">✓✓</span>' if is_read else '<span style="color:#ccc;">✓</span>'

                    bubble_cls  = "me" if is_me else "them"
                    wrap_cls    = "me" if is_me else ""
                    bubble_extra = ' bubble-del' if is_deleted else ''

                    if is_me:
                        msg_col, del_col = st.columns([20, 1])
                    else:
                        del_col_empty, msg_col = st.columns([1, 20])

                    with msg_col:
                        st.markdown(
                            f'<div class="msg-wrap {wrap_cls}">'
                            f'{avatar_html(row["sender"],"av-sm") if not is_me else ""}'
                            f'<div>'
                            f'<div class="bubble {bubble_cls}{bubble_extra}">{content}</div>'
                            f'<div class="bubble-meta">{time_str} {tick}</div>'
                            f'</div>'
                            f'{avatar_html(row["sender"],"av-sm") if is_me else ""}'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

                    if is_me and not is_deleted:
                        with del_col:
                            st.markdown('<div class="del-btn">', unsafe_allow_html=True)
                            if st.button("🗑", key=f"del_{idx}", help="Delete"):
                                delete_message(conn, me, contact, row["timestamp"])
                                st.rerun()
                            st.markdown("</div>", unsafe_allow_html=True)

        # Input
        prompt = st.chat_input(f"Message {contact}…")
        if prompt and prompt.strip():
            send_message(conn, me, contact, prompt.strip())
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# SEARCH PAGE
# ─────────────────────────────────────────────────────────────────────────────
def page_search(conn):
    me = st.session_state.username
    st.markdown('<h2 style="color:#1a1a2e;margin:0.5rem 0 1rem;">🔍 Search Users</h2>', unsafe_allow_html=True)
    query = st.text_input("", placeholder="Type a username to search…", key="sq", label_visibility="collapsed")

    if query.strip():
        users_df    = fetch_users(conn)
        requests_df = fetch_requests(conn)
        results = users_df[
            users_df["username"].str.contains(query.strip(), case=False, na=False) &
            (users_df["username"] != me)
        ]
        if results.empty:
            st.info("No users found.")
        else:
            for _, row in results.iterrows():
                user = row["username"]
                already_sent = already_accepted = False
                if not requests_df.empty:
                    fwd = requests_df[(requests_df["from_user"]==me)&(requests_df["to_user"]==user)]
                    bwd = requests_df[(requests_df["from_user"]==user)&(requests_df["to_user"]==me)]
                    if not fwd.empty:
                        already_sent     = fwd.iloc[0]["status"] == "pending"
                        already_accepted = fwd.iloc[0]["status"] == "accepted"
                    if not bwd.empty and bwd.iloc[0]["status"] == "accepted":
                        already_accepted = True

                c1, c2 = st.columns([5,1])
                with c1:
                    st.markdown(
                        f'<div class="sc-card">{avatar_html(user,"av")}'
                        f'<div><div class="sc-card-name">{user}</div>'
                        f'<div class="sc-card-sub">StreamConnect user</div></div></div>',
                        unsafe_allow_html=True,
                    )
                with c2:
                    if already_accepted:   st.success("✅ Friends")
                    elif already_sent:     st.info("⏳ Pending")
                    else:
                        if st.button("➕ Add", key=f"add_{user}"):
                            send_friend_request(conn, me, user)
                            st.success(f"Request sent to {user}!")
                            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# FRIEND REQUESTS PAGE
# ─────────────────────────────────────────────────────────────────────────────
def page_requests(conn):
    me = st.session_state.username
    st.markdown('<h2 style="color:#1a1a2e;margin:0.5rem 0 1rem;">👥 Friend Requests</h2>', unsafe_allow_html=True)
    requests_df = fetch_requests(conn)
    tab_in, tab_out = st.tabs(["📥 Incoming", "📤 Outgoing"])

    with tab_in:
        incoming = pd.DataFrame()
        if not requests_df.empty:
            incoming = requests_df[(requests_df["to_user"]==me)&(requests_df["status"]=="pending")]
        if incoming.empty:
            st.markdown('<p style="color:#65676b;">No incoming requests.</p>', unsafe_allow_html=True)
        else:
            for _, row in incoming.iterrows():
                c1, c2 = st.columns([5,1])
                with c1:
                    st.markdown(
                        f'<div class="sc-card">{avatar_html(row["from_user"],"av")}'
                        f'<div><div class="sc-card-name">{row["from_user"]}</div>'
                        f'<div class="sc-card-sub">Wants to connect with you</div></div></div>',
                        unsafe_allow_html=True,
                    )
                with c2:
                    if st.button("✅ Accept", key=f"acc_{row['from_user']}"):
                        accept_friend_request(conn, row["from_user"], me)
                        st.success(f"Now friends with {row['from_user']}!")
                        st.rerun()

    with tab_out:
        outgoing = pd.DataFrame()
        if not requests_df.empty:
            outgoing = requests_df[requests_df["from_user"]==me]
        if outgoing.empty:
            st.markdown('<p style="color:#65676b;">No outgoing requests.</p>', unsafe_allow_html=True)
        else:
            for _, row in outgoing.iterrows():
                c = "#31a24c" if row["status"]=="accepted" else "#f0a500"
                badge = "✅ Accepted" if row["status"]=="accepted" else "⏳ Pending"
                st.markdown(
                    f'<div class="sc-card">{avatar_html(row["to_user"],"av")}'
                    f'<div><div class="sc-card-name">{row["to_user"]}</div>'
                    f'<div class="sc-card-sub" style="color:{c};">{badge}</div></div></div>',
                    unsafe_allow_html=True,
                )


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    init_session()
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.markdown(STYLES, unsafe_allow_html=True)

    if not st.session_state.authenticated:
        if st.session_state.auth_page == "login": page_login(conn)
        else: page_signup(conn)
        return

    top_nav(conn)

    nav = st.session_state.nav
    if   nav == "chat":    page_chat(conn)
    elif nav == "search":  page_search(conn)
    elif nav == "request": page_requests(conn)


if __name__ == "__main__":
    main()
