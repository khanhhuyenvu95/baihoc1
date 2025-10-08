# --- CHỨC NĂNG 6: KHUNG CHAT TƯƠNG TÁC VỚI GEMINI ---
st.markdown("---")
st.subheader("💬 Trò chuyện trực tiếp với Gemini AI")

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    # Tạo client Gemini
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.5-flash"

    # Lưu lịch sử hội thoại
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Hiển thị lịch sử hội thoại
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    # Ô nhập chat
    user_input = st.chat_input("Nhập câu hỏi hoặc yêu cầu của bạn...")

    if user_input:
        # Hiển thị tin nhắn người dùng
        st.chat_message("user").markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Gửi tới Gemini
        with st.chat_message("assistant"):
            with st.spinner("Gemini đang suy nghĩ..."):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=user_input
                    )
                    reply = response.text
                except Exception as e:
                    reply = f"❌ Lỗi khi gọi API Gemini: {e}"

                st.markdown(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
else:
    st.warning("⚠️ Chưa thiết lập GEMINI_API_KEY trong Secrets. Vui lòng cấu hình trước khi dùng Chat.")
