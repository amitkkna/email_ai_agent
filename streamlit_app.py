import streamlit as st
from gmail_utils import authenticate_gmail, get_unread_emails, get_email_content, send_email, mark_as_read
from openai_utils import summarize_and_reply

st.set_page_config(page_title="AI Email Assistant", layout="wide")
st.title("📬 AI Email Assistant")

if "gmail_service" not in st.session_state:
    st.session_state.gmail_service = authenticate_gmail()

service = st.session_state.gmail_service
emails = get_unread_emails(service)

if not emails:
    st.info("No unread emails found.")
else:
    for i, email in enumerate(emails):
        msg_id = email['id']
        subject, sender, body = get_email_content(service, msg_id)
        summary, reply = summarize_and_reply(subject, sender, body)

        with st.expander(f"📩 {subject} — {sender}", expanded=False):
            st.markdown(f"**Email Body:**\n```\n{body}\n```")
            st.markdown(f"**Summary:**\n{summary}")
            st.text_area("Suggested Reply:", value=reply, key=f"reply_text_{i}", height=150)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✅ Approve & Send", key=f"approve_{i}"):
                    send_email(service, sender, subject, st.session_state[f"reply_text_{i}"])
                    mark_as_read(service, msg_id)
                    st.success("Reply sent!")
            with col2:
                if st.button("❌ Skip", key=f"skip_{i}"):
                    mark_as_read(service, msg_id)
                    st.warning("Skipped.")
