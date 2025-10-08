import streamlit as st
from google import genai
from google.genai import types

# --- CHỨC NĂNG 6: KHUNG CHAT TƯƠNG TÁC VỚI GEMINI ---
st.markdown("---")
st.subheader("💬 Trò chuyện trực tiếp với Gemini AI")

api_key = st.secrets.get("GEMINI_API_KEY")
model_name = "gemini-2.5-flash"

if api_key:
    # --- Khởi tạo Client và Chat Session ---
    try:
        # Tạo client Gemini
        client = genai.Client(api_key=api_key)

        # Khởi tạo hoặc lấy đối tượng Chat từ session_state
        if "chat_session" not in st.session_state:
            # Tạo một session chat mới với model được chọn
            st.session_state.chat_session = client.chats.create(
                model=model_name
            )
            # Khởi tạo lịch sử hiển thị
            st.session_state.chat_history = []
            
    except Exception as e:
        st.error(f"❌ Không thể tạo Client hoặc Chat Session: {e}")
        st.stop() # Dừng chạy nếu không thể kết nối

    # --- Hiển thị Lịch sử Hội thoại ---
    # Lấy lịch sử hiển thị đã lưu
    for message in st.session_state.chat_history:
        # Sử dụng API của Streamlit để hiển thị tin nhắn dựa trên vai trò
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- Ô Nhập và Xử lý Tin nhắn Mới ---
    # Ô nhập chat luôn ở dưới cùng
    user_input = st.chat_input("Nhập câu hỏi hoặc yêu cầu của bạn...")

    if user_input:
        # 1. Hiển thị tin nhắn người dùng mới
        st.chat_message("user").markdown(user_input)
        # Lưu vào lịch sử hiển thị
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # 2. Gửi tin nhắn tới Gemini và nhận phản hồi
        with st.chat_message("assistant"):
            with st.spinner("Gemini đang suy nghĩ..."):
                try:
                    # Gửi tin nhắn qua đối tượng chat session đã tạo
                    response = st.session_state.chat_session.send_message(user_input)
                    reply = response.text
                except Exception as e:
                    # Xử lý lỗi trong quá trình gửi tin nhắn
                    reply = f"❌ Lỗi khi gửi tin nhắn đến Gemini: {e}"

            # 3. Hiển thị phản hồi và lưu vào lịch sử
            st.markdown(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

else:
    # Cảnh báo nếu API Key chưa được thiết lập
    st.warning("⚠️ Chưa thiết lập **GEMINI_API_KEY** trong Streamlit Secrets. Vui lòng cấu hình trước khi dùng Chat.")
