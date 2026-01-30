# -*- coding: utf-8 -*-
"""
Supabase Storage 上傳檔案範例（官方推薦寫法）
支援 jpg / png，從本地檔案上傳
使用 .env 載入設定
"""

import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# =============================================
# 載入 .env
# =============================================
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME  = os.getenv("BUCKET_NAME", "pgbug_doc")

# 基本檢查
if not all([SUPABASE_URL, SUPABASE_KEY]):
    print("錯誤：.env 缺少 SUPABASE_URL 或 SUPABASE_KEY")
    print("請確認已使用 service_role key（而非 anon key）")
    exit(1)

print("設定載入完成：")
print(f"  URL    : {SUPABASE_URL}")
print(f"  Bucket : {BUCKET_NAME}")
print("-" * 50)

# =============================================
# 初始化 Supabase client
# =============================================
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("Supabase client 初始化完成")

# =============================================
# 上傳函式（官方推薦寫法）
# =============================================
def upload_file_to_supabase(
    local_path: str,
    bucket_folder: str = "bug_screenshots",
    upsert: bool = False,           # 是否允許覆蓋同名檔案
    cache_control: str = "3600"     # 快取秒數（可選）
) -> tuple:
    """
    上傳本地檔案到 Supabase Storage
    回傳：(成功與否, 公開網址 或 錯誤訊息)
    """
    if not os.path.exists(local_path):
        return False, f"本地檔案不存在：{local_path}"

    filename = os.path.basename(local_path)
    name, ext = os.path.splitext(filename)
    ext = ext.lower().lstrip(".")

    if ext not in ["jpg", "jpeg", "png"]:
        return False, "只支援 jpg / jpeg / png 格式"

    # 產生唯一檔名（避免衝突）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    storage_filename = f"{bucket_folder}/{timestamp}_{name}.{ext}"

    # 決定 content-type
    content_type = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"

    print(f"開始上傳：")
    print(f"  本地     : {local_path}")
    print(f"  目標路徑 : {storage_filename}")
    print(f"  MIME     : {content_type}")

    try:
        with open(local_path, "rb") as file:
            response = supabase.storage \
                .from_(BUCKET_NAME) \
                .upload(
                    path=storage_filename,                  # bucket 內路徑 + 檔名
                    file=file,                              # 已開啟的 binary file
                    file_options={
                        "content-type": content_type,
                        "cache-control": cache_control,
                        "upsert": str(upsert).lower()       # "true" 或 "false"
                    }
                )

        # 如果 bucket 是 public，可直接取公開 URL
        public_url_data = supabase.storage \
            .from_(BUCKET_NAME) \
            .get_public_url(storage_filename)

        public_url = public_url_data.get("publicUrl") if isinstance(public_url_data, dict) else public_url_data

        print("上傳成功！")
        print(f"公開網址：{public_url}")
        return True, public_url

    except Exception as e:
        error_str = str(e)
        print("上傳失敗：")
        print(error_str)
        
        if "403" in error_str or "Unauthorized" in error_str or "Invalid Compact JWS" in error_str:
            print("\n*** 常見原因與解決 ***")
            print("1. 使用的是 anon key 而非 service_role key → 請換成 service_role key")
            print("2. key 複製時有空格/換行 → 重新貼上完整 key")
            print("3. Storage 政策不允許寫入 → Dashboard → Storage → Policies 檢查")
        
        return False, error_str


# =============================================
# 執行測試
# =============================================
if __name__ == "__main__":
    # 請改成你真實的測試圖片路徑
    test_file = r"C:\ai_project2\eshop_bug_list\bak\test_bug.png"

    if not os.path.exists(test_file):
        print(f"測試檔案不存在，請修改路徑：{test_file}")
    else:
        success, result = upload_file_to_supabase(
            local_path=test_file,
            bucket_folder="bug_reports",    # 可自訂資料夾
            upsert=False                    # 不覆蓋（預設）
        )
        
        if success:
            print("\n上傳完成，可在瀏覽器直接開啟：")
            print(result)
        else:
            print("\n請修正問題後再試一次。")