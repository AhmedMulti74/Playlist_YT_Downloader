from flask import Flask, render_template, request
import os
import yt_dlp

app = Flask(__name__)

# مسار التحميل الافتراضي
DOWNLOAD_FOLDER = r'C:\Users\elmou\Downloads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_playlist():
    playlist_url = request.form.get('url')  # استخدم get للحصول على القيمة
    video_quality = request.form.get('quality')  # استخدم get للحصول على الجودة

    # التحقق من وجود القيم المدخلة
    if not playlist_url:
        return "يرجى إدخال رابط قائمة التشغيل."
    
    if video_quality is None or video_quality == "":  # تحقق من الجودة
        return "يرجى اختيار جودة الفيديو الصحيحة."
    
    # التحقق من صحة الجودة المختارة
    valid_qualities = ['360', '480', '720', '1080']
    if video_quality not in valid_qualities:
        return "يرجى اختيار جودة الفيديو الصحيحة."

    try:
        # إعدادات yt-dlp
        ydl_opts = {
            'format': f'bestvideo[height<={video_quality}]+bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
            }],
            'merge_output_format': 'mp4',
            'noplaylist': False,  # لضمان تحميل قائمة التشغيل بالكامل
        }

        # تأكد من أن المجلد موجود
        if not os.path.exists(DOWNLOAD_FOLDER):
            os.makedirs(DOWNLOAD_FOLDER)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=True)

        if result is None:
            return "حدث خطأ أثناء محاولة تحميل الفيديو: الرابط غير صالح أو لا يحتوي على فيديو."

        return "تم تحميل قائمة التشغيل بنجاح!"
    
    except Exception as e:
        return f"حدث خطأ أثناء محاولة تحميل قائمة التشغيل: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
