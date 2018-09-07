import os,sys




BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.insert(0,BASE_DIR)

SPEACK_FILE = os.path.join(BASE_DIR,"database\\speak\\test.wav")
LISTEN_FILE =os.path.join(BASE_DIR,"database\\listen\\1kXF.wav")
PLAY_MEDIA = r"D:/ffmpeg/bin/ffplay"
TRANSVERTER=r"D:/ffmpeg/bin/ffmpeg"

SDK_FILE =r"E:\Windows_aisound_exp1208_aitalk_exp1208_awaken_exp1208_iat1208_tts_online1208_5b559fed\bin\msc_x64.dll"

THRESHOLD = 0.5  #本地数据库识别可信度阈值

Tulin_API_KEY = "164391ebc59c48a88c7c4cc41682e5a3"
SYNO_FILES=os.path.join(BASE_DIR,'synom\\new_synomys.json')

#百度token配置参数
Grant_type = "client_credentials"
Client_id = "6vnvj2pvAFfbUVcXuUoW4YeD"
Client_secret = "Vm7fHywZubDqk2oNKNG9OpF5QTNtL5hG"