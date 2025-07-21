import streamlit as st
from groq import Groq
from database import create_table, save_content, get_all_records, delete_record

# === Initialize Database ===
create_table()

# === API Key & Client ===
groq_api_key = "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"
client = Groq(api_key=groq_api_key)

# === UI Header ===
st.title("🔥 YouTube Shorts Hook & Script Generator")
st.markdown("Generate catchy **hooks**, **scripts**, and **captions** in seconds!")

# === User Input ===
col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("Choose Platform", ["YouTube", "Instagram", "Both"])
    language = st.selectbox("Choose Language", ["English", "Hindi"])
with col2:
    topic = st.text_input("🎯 Enter Topic (e.g. AI Tools, Fitness Tips):")
    num_hooks = st.slider("Number of Hooks", 1, 10, 5)

video_summary = st.text_area("🧠 Video Summary (Optional)")

# === Prompt Builder ===
def build_prompt(section, topic, language, num_hooks, summary=""):
    lang_tag = "in Hindi" if language == "Hindi" else "in English"
    context = f" The video is about: {summary}" if summary else ""

    if section == "hooks":
        return f"You're a viral short-form content creator. Give me {num_hooks} super catchy hooks for {topic}.{context} {lang_tag}. Each hook under 12 words."
    elif section == "script":
        return f"Create a 60-word viral script for a {platform} short video on {topic}.{context} {lang_tag}. Use informal, relatable tone."
    elif section == "caption":
        return f"Write an engaging caption under 100 characters for a short video on {topic}.{context} {lang_tag}."

# === Generate Button ===
if st.button("🚀 Generate Content"):
    if not topic:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Generating using Groq..."):
            hook_prompt = build_prompt("hooks", topic, language, num_hooks, video_summary)
            script_prompt = build_prompt("script", topic, language, num_hooks, video_summary)
            caption_prompt = build_prompt("caption", topic, language, num_hooks, video_summary)

            hooks = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": hook_prompt}]
            ).choices[0].message.content.strip()

            script = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": script_prompt}]
            ).choices[0].message.content.strip()

            caption = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": caption_prompt}]
            ).choices[0].message.content.strip()

            # Save to DB
            save_content(topic, language, hooks, script, caption, platform, video_summary)

            # === Display Output ===
            st.subheader("🌟 Hooks")
            st.code(hooks)

            st.subheader("🎬 Script")
            st.code(script)

            st.subheader("🗘️ Caption")
            st.code(caption)

# === View Saved Shorts with Hide/Show ===
st.markdown("---")
st.subheader("📚 Your Saved Shorts")

show_saved = st.checkbox("👁️ Show Saved Shorts", value=False)

if show_saved:
    if st.button("🔄 Refresh Records"):
        st.experimental_rerun()

    records = get_all_records()

    if records:
        topics = sorted(list(set([r[1] for r in records])))
        platforms = sorted(list(set([r[6] for r in records if r[6]])))

        col1, col2 = st.columns(2)
        with col1:
            selected_topic = st.selectbox("Filter by Topic", ["All"] + topics)
        with col2:
            selected_platform = st.selectbox("Filter by Platform", ["All"] + platforms)

        search_keyword = st.text_input("🔍 Search keywords in Hook/Script/Caption")

        for record in records:
            id, topic, lang, hooks, script, caption, platform, summary, timestamp = record

            topic_match = (selected_topic == "All" or topic == selected_topic)
            platform_match = (selected_platform == "All" or platform == selected_platform)
            keyword_match = any(search_keyword.lower() in section.lower() for section in [hooks, script, caption])

            if topic_match and platform_match and (not search_keyword or keyword_match):
                st.markdown(f"**🕒 {timestamp} | 🎯 {topic} | 🌐 {platform} | 🗣️ {lang}**")
                st.markdown(f"**🧠 Summary:** {summary}")
                st.markdown(f"**🌟 Hooks:**\n{hooks}")
                st.markdown(f"**🎬 Script:**\n{script}")
                st.markdown(f"**🗘️ Caption:**\n{caption}")

                if st.button(f"🚨 Delete", key=f"delete_{id}"):
                    delete_record(id)
                    st.success("Deleted!")
                    st.experimental_rerun()

                st.markdown("---")
    else:
        st.info("No saved content yet.")
