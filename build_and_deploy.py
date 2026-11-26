#!/usr/bin/env python3
"""Build KoreanGo 5-language showcase, /privacy, and /support pages, bundle Cloudflare Worker, and deploy to https://koreango.appengine.fun."""
from __future__ import annotations

import argparse
import base64
import html as html_mod
import json
import os
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
IMG_DIR = PUBLIC_DIR / "images"
AUD_DIR = PUBLIC_DIR / "audio"

ACCOUNT_ID = "9fb3b494e6d4d659f2cf567efb94fc38"
ZONE_ID = "977b0b4fa0ab6e587b8758a04016c5e8"
SCRIPT_NAME = "koreango-site"
HOSTNAME = "koreango.appengine.fun"
ORIGIN = f"https://{HOSTNAME}"
# Live Apple App Store numeric ID for com.chiangkevin.koreango
APP_STORE_ID = "6838241626"
APP_STORE_URL = f"https://apps.apple.com/app/id{APP_STORE_ID}" if APP_STORE_ID else ""

CONTENT = {
    "en": {
        "html_lang": "en",
        "title": "KoreanGo — Travel Korean, 100 Seoul Video Dialogues, Voice Practice & Live Translation",
        "desc": "Master real-life travel Korean with 15 lessons, 100 Seoul travel video dialogues, 40 Hangul Jamo stroke practice, 24 minimal pairs, Guided Voice Practice, and Live Two-Way Translation.",
        "keywords": "KoreanGo,travel Korean,Hangul,Jamo,Korean pronunciation,minimal pairs,Seoul travel dialogues,live voice translation,learn Korean,AE Interactive",
        "nav_privacy": "Privacy",
        "nav_support": "Support",
        "nav_download": "Get App" if APP_STORE_URL else "View Plans",
        "hero_badge": "15 LESSONS · 100 SEOUL VIDEO DIALOGUES · LIVE TRANSLATION · ZERO ADS",
        "hero_title": "Speak Real Korean <span>Before Your Flight Lands</span>",
        "hero_sub": "From 40 Hangul Jamo strokes, 24 minimal pair sound drills, and 100 real-life Seoul travel video dialogues to 12-scene Guided Voice Practice and live two-way voice translation—with zero accounts and zero tracking.",
        "status_pill": (
            "Available Now on App Store · iPhone, iPad & iPhone Duo"
            if APP_STORE_URL
            else "Built Native for iPhone & iPad · iOS 17+ · Start Free ($3.99 Optional Pro)"
        ),
        "cta_store_sub": "Download Free on",
        "cta_store_main": "App Store",
        "cta_coming_main": "Coming Soon · App Store",
        "cta_audio": "▶ Hear Native Phrases",
        "cta_screens": "Explore Screens ↓",
        "cta_plans": "See Free vs. $3.99 Pro ↓",
        "sec_audio_badge": "REAL IN-APP STUDIO AUDIO · REVISED ROMANIZATION & IPA",
        "sec_audio_title": "Hear Everyday Seoul Korean as It's Spoken",
        "sec_audio_sub": "Actual MP3 clips bundled inside KoreanGo—highlighting tense consonants (tt), natural liaison, and practical travel etiquette.",
        "btn_play": "Play",
        "btn_playing": "Playing",
        "sec_screens_badge": "LIVE APP PREVIEWS · IPHONE 6.9\" & IPAD 13\"",
        "sec_screens_title": "Designed for One-Handed Travel Confidence",
        "sec_screens_sub": "Clean portrait typography sized for readability across busy Seoul Metro platforms, cafés, and airport counters—plus full iPad 13\" support.",
        "screens_labels": [
            "15-Lesson Travel Path",
            "12-Scene Voice Practice",
            "Live 2-Way Interpreter",
            "100 Seoul Video Dialogues",
            "40 Jamo & 24 Minimal Pairs",
            "iPad 13\" Display",
        ],
        "sec_features_badge": "SIX INTEGRATED MODULES",
        "sec_features_title": "Everything You Need in One Offline-Ready App",
        "features": [
            ("📚", "15 Guided Lessons & 18 Grammar Drills", "Progress smoothly from Hangul vowels and batchim rules through café orders, BBQ dining, Olive Young tax refunds, Seoul Metro transfers, hotels, and clinics."),
            ("🎬", "100 Seoul Travel Video Dialogues", "Real-life Korea travel conversations across 5 categories with 200 dual-speaker studio clips, Revised Romanization, Seoul IPA, and cultural notes."),
            ("💬", "12-Scene Guided Voice Practice & Free Talk", "On-device interactive roleplay: Korean staff speaks first, helpful phrase cards stay onscreen while you talk, and you complete 3 real travel tasks."),
            ("🗣️", "Live Two-Way Voice Translation", "Speak or type between English, Traditional Chinese, Simplified Chinese, Japanese, or Spanish and Korean—complete with fullscreen show-the-clerk cards."),
            ("✍️", "40 Jamo Strokes, 24 Pairs & 160 SRS Flashcards", "Interactive Hangul writing canvas, plain vs. aspirated vs. tense ear drills, 693 studio MP3s, and Standard / Large / Extra Large font scaling."),
            ("🔒", "Zero Sign-In · Local Privacy Only", "No accounts, no ads, and zero third-party SDKs. Study streaks, Jamo mastery, and flashcards stay strictly inside iOS UserDefaults on your device."),
        ],
        "sec_pricing_badge": "NO SUBSCRIPTIONS · START FREE",
        "sec_pricing_title": "Free Essentials. One-Time $3.99 Upgrade.",
        "sec_pricing_sub": "Master Hangul and essential travel phrases for free—then unlock all 15 lessons and 100 videos forever with a single buyout.",
        "free_tier_tag": "KOREANGO FREE",
        "free_tier_title": "Free Forever",
        "free_tier_price": "$0",
        "free_tier_items": [
            "Complete 40 Hangul Jamo chart & interactive stroke canvas",
            "All 24 minimal pairs (3-way plain / aspirated / tense drills)",
            "All 160 SM-2 flashcards & 4 interactive quiz modes",
            "Lessons 1–3 + 10 travel videos + daily Voice Practice (5/day) & Interpreter (8/day)",
        ],
        "pro_tier_badge": "ONE-TIME BUYOUT · NO SUBSCRIPTION",
        "pro_tier_title": "KoreanGo Pro Lifetime",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "All 15 guided travel lessons unlocked (Lessons 4–15)",
            "All 100 Seoul travel video dialogues & 200 studio recordings",
            "Unlimited 12-scene Voice Practice roleplay & Free Talk",
            "Unlimited two-way Live Voice Interpreter (offline-ready)",
        ],
        "bottom_cta_title": "Ready for Your Next Trip to Seoul?",
        "bottom_cta_sub": "Free foundation on iPhone & iPad—zero sign-up, zero subscriptions, built purely in Swift.",
        "appstore_btn_label": "Download Free on App Store" if APP_STORE_URL else "Explore Free Tier Modules ↑",
        "coming_soon_btn": "Pre-Release v1.0 · Contact Support",
        "privacy_title": "Privacy Policy — KoreanGo",
        "privacy_updated": "Last Updated: November 23, 2026",
        "privacy_sections": [
            ("1. Zero Account & Zero Personal Data Collection", "KoreanGo is developed by AE Interactive (AppEngine Interactive). We require no account registration and never collect, store, sell, or transmit personal data to AE Interactive servers (App Store Privacy Nutrition Label: Data Not Collected / NSPrivacyTracking = false). Study progress, Hangul mastery, SRS intervals, streaks, and font sizes are stored locally on your device via Apple UserDefaults (Required Reason API CA92.1)."),
            ("2. Microphone, Speech Recognition & On-Device Processing", "Microphone and speech recognition permissions (NSMicrophoneUsageDescription / NSSpeechRecognitionUsageDescription) are requested strictly on demand when you tap Record in Voice Practice or Live Interpreter. Translations and guided roleplay run through Apple's native on-device Speech, Translation, and system language frameworks."),
            ("3. No Ads, No Analytics, No Tracking", "KoreanGo bundles zero advertising networks, zero third-party telemetry SDKs, and zero cross-app tracking."),
            ("4. Contact Us", "Questions or feedback? Email AE Interactive anytime at help@appengine.fun."),
        ],
        "support_title": "Support & Compatibility — KoreanGo",
        "support_sub": "Quick help for Guided Voice Practice, Offline Translation Packs, and App Support.",
        "support_cards": [
            ("On-Device Guided Voice Practice Compatibility", "Uses Apple's native on-device system language architecture on supported hardware (iPhone 15 Pro / Pro Max, iPhone 16 series, iPhone 17 series or newer, and M-series / A17 Pro+ iPads running iOS / iPadOS 26.0+ with system features enabled), with built-in phrase matching fallback on supported iOS 17+ devices."),
            ("100% Offline Courses, 100 Videos & 693 Studio MP3s", "All 15 units, 40 Hangul Jamo stroke guides, 24 minimal pairs, 5 phonology rules, 160 flashcards, 18 grammar drills, and 100 Seoul scenario videos work offline on any iPhone or iPad running iOS 17.0+ without signing in."),
            ("Download Korean Offline Translation Packs", "Live Two-Way Interpreter uses Apple's native Translation framework. Before your flight to Incheon or Gimpo, open iOS Settings -> Apps -> Translate (or follow the in-app prompt) to download Korean offline translation packs."),
            ("Direct Developer Support", "Email AE Interactive at help@appengine.fun — we typically respond within 24 hours."),
        ],
        "footer_rights": "© 2026 AE Interactive. All rights reserved.",
        "studio_link_label": "AE Interactive Studio",
    },
    "zh-Hant": {
        "html_lang": "zh-Hant",
        "title": "KoreanGo — 首爾旅遊韓語、100 個實境對話影片、互動口說與雙向語音口譯",
        "desc": "從 40 個韓文字母筆順、24 組平音激音緊音辨音、100 個首爾旅遊實境對話影片，到 12 情境互動口說與繁中／韓語即時雙向語音翻譯，免登入零追蹤。",
        "keywords": "KoreanGo,韓語學習,韓國旅遊韓文,首爾自由行韓語,四十音,韓語三組對立音,韓國旅遊實境對話,即時韓文口譯,AE Interactive",
        "nav_privacy": "隱私權政策",
        "nav_support": "支援與常見問題",
        "nav_download": "立即下載" if APP_STORE_URL else "查看方案",
        "hero_badge": "15 堂系統課 · 100 個首爾實境對話 · 即時雙向口譯 · 零廣告追蹤",
        "hero_title": "飛抵仁川前，<span>先開口說出道地韓國旅遊會話</span>",
        "hero_sub": "從 40 個韓文字母手寫筆順與 24 組平／激／緊音辨音打底，搭配 100 個首爾實境對話短片、店員主動發問口說模擬與現場雙向語音翻譯——全程免註冊、零廣告。",
        "status_pill": (
            "App Store 正式上架 · 免費下載體驗 · iPhone、iPad 與 iPhone Duo"
            if APP_STORE_URL
            else "專為 iPhone 與 iPad 原生打造 · iOS 17+ · 核心免費暢學"
        ),
        "cta_store_sub": "立即前往下載",
        "cta_store_main": "App Store",
        "cta_coming_main": "即將上架 · App Store",
        "cta_audio": "▶ 試聽原生發音",
        "cta_screens": "瀏覽實機畫面 ↓",
        "cta_plans": "查看免費與 $3.99 Pro ↓",
        "sec_audio_badge": "收錄真實 App 錄音室語音 · 標註音變與羅馬拼音",
        "sec_audio_title": "點一下，立即試聽道地首爾旅遊韓語",
        "sec_audio_sub": "直接試聽 KoreanGo 內建 693 支錄音室音檔精選——帶你聽懂緊音（ㄸ）、連音（갈아타요）與輕聲弱化等旅遊發音重點。",
        "btn_play": "播放",
        "btn_playing": "播放中",
        "sec_screens_badge": "實機畫面精選 · IPHONE 6.9\" 與 IPAD 13\"",
        "sec_screens_title": "單手直式大字體，地鐵月台一眼看懂",
        "sec_screens_sub": "專為韓國自由行單手操作打造，支援標準／大字／特大三段字級調整與 iPad 13 吋大螢幕排版。",
        "screens_labels": [
            "15 堂系統學習路徑",
            "12 情境實戰互動口說",
            "首爾現場 · 雙向語音口譯",
            "100 個首爾旅遊實境對話",
            "40 字母筆順與 24 組辨音",
            "iPad 13 吋寬螢幕實戰",
        ],
        "sec_features_badge": "六大實戰模組",
        "sec_features_title": "從韓文字母到明洞救急，一套全搞定",
        "features": [
            ("📚", "15 堂旅遊路線 ＋ 18 堂文法特訓", "從母音、子音與收尾音（Batchim）起步，涵蓋咖啡烤肉點餐、美妝即時退稅、地鐵 2 號線轉乘、飯店入住與醫院急救。"),
            ("🎬", "100 個首爾旅遊實境對話影片（200 句錄音）", "五大韓國場景×四階段旅遊時間線，完整收錄標準羅馬拼音、全句首爾音標 IPA、語法提示與三語對照。"),
            ("💬", "12 情境實戰互動對話 ＋ 自由對話", "採用裝置端互動引導：先由韓國店員主動提問，錄音練習時畫面貼心保留關鍵句提示，陪你完成 3 關現場任務。"),
            ("🗣️", "現場雙向即時語音口譯（底部最右一鍵直達）", "支援繁中／簡中／英文／日文／西文 ↔ 韓語即時語音與文字互譯，並附全螢幕「給韓國店員看」特大字卡。"),
            ("✍️", "40 字母筆順畫板、24 組辨音與 160 SRS 單字", "互動筆順描紅、平音／激音／緊音三組對立音盲測、693 支錄音室 MP3 音檔與三段字級切換。"),
            ("🔒", "免登入註冊・100% 本機隱私", "無廣告聯播網、無第三方追蹤碼（NSPrivacyTracking = false），所有進度與單字紀錄僅存於您的裝置本機。"),
        ],
        "sec_pricing_badge": "無月費訂閱制 · 基礎免費暢學",
        "sec_pricing_title": "免費打好韓語基礎 · $3.99 一次永久買斷",
        "sec_pricing_sub": "免費學完 40 個字母、24 組辨音與前 3 課後，需要全 100 支首爾實境短片與無限口譯時再單次解鎖即可。",
        "free_tier_tag": "KOREANGO 免費版",
        "free_tier_title": "永久免費版",
        "free_tier_price": "免費 $0",
        "free_tier_items": [
            "完整 40 韓文字母圖表、雙速發音與筆順互動畫板",
            "完整 24 組平音／激音／緊音最小對立對聽力挑戰",
            "完整 160 單字 SM-2 記憶卡與 4 大互動測驗模式",
            "第 1–3 堂課 ＋ 10 支實境短片 ＋ 每日免費口說(5次)與口譯(8次)",
        ],
        "pro_tier_badge": "一次買斷 · 終身無訂閱自動扣款",
        "pro_tier_title": "KoreanGo Pro 永久買斷",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "完整解鎖全部 15 堂韓國旅遊實戰課程（第 4–15 課）",
            "解鎖全 100 部首爾實境對話影片與 200 句真人錄音",
            "12 大韓國旅遊情境店員口說模擬與自由對話無限次",
            "現場雙向即時語音口譯無限次使用（支援離線翻譯包）",
        ],
        "bottom_cta_title": "下一趟首爾旅行，帶這套就夠了",
        "bottom_cta_sub": "iPhone 與 iPad 專屬原生體驗・免註冊登入・隨時開啟練習。",
        "appstore_btn_label": "前往 App Store 免費下載" if APP_STORE_URL else "查看免費完整功能 ↑",
        "coming_soon_btn": "即將上架 App Store · 技術支援",
        "privacy_title": "KoreanGo 隱私權政策",
        "privacy_updated": "最後更新日期：2026 年 11 月 23 日",
        "privacy_sections": [
            ("1. 無帳號登入與不收集個人資料", "KoreanGo 由 AE Interactive（AppEngine Interactive）開發。本 App 無需註冊帳號，不會收集、儲存、出售或傳輸任何個人識別資料至開發者伺服器（App Store Privacy 宣告「不收集任何資料」，NSPrivacyTracking = false）。所有進度、單字複習週期與字級設定皆僅透過標準 Apple UserDefaults（Required Reason API CA92.1）存於您的裝置本機。"),
            ("2. 麥克風、語音辨識與裝置端處理", "僅在您主動點擊「情境對話練習」或「雙向即時口譯」麥克風按鈕時才會請求權限；語音辨識（ko-KR）、Apple 本機翻譯套件與裝置端對話引導皆以本機優先執行，不會將對話上傳至任何第三方伺服器。"),
            ("3. 零廣告與零第三方追蹤", "本 App 不包含任何廣告 SDK、商業分析 SDK 或跨 App 行為追蹤。"),
            ("4. 聯絡我們", "如有隱私權問題，歡迎寄信至 help@appengine.fun。"),
        ],
        "support_title": "支援服務與常見問題 — KoreanGo",
        "support_sub": "互動對話相容機型、韓語離線翻譯包下載與技術支援窗口。",
        "support_cards": [
            ("互動對話與裝置端相容性", "支援搭載 Apple 裝置端系統語言架構之機型（iPhone 15 Pro / Pro Max、iPhone 16 / 17 系列以上或 M 系列／A17 Pro 以上 iPad，系統為 iOS / iPadOS 26.0+ 並於設定開啟對應功能）；所有 iOS 17+ 機型皆提供即時韓語句型引導備援練習。"),
            ("離線課程、100 支短片與 693 支錄音室音檔", "全部 15 堂課程、40 個字母筆順、24 組三組對立音辨音、100 部首爾實境短片、160 張單字卡與 18 堂文法皆可離線運作，不需帳號也不限機型（支援 iOS 17.0+）。"),
            ("出發前預載韓語離線翻譯包", "「現場雙向即時口譯」採用 Apple 原生 Translation 框架；出發飛往仁川或金浦前，建議先到「系統設定 → App → 翻譯」下載「繁體中文 ↔ 韓語」離線包，地下鐵或沒網路也能流暢對話。"),
            ("聯絡客服團隊", "若有任何建議或問題，請寄信至 help@appengine.fun，AE Interactive 團隊通常於 24 小時內回覆。"),
        ],
        "footer_rights": "© 2026 AE Interactive. 保留所有權利。",
        "studio_link_label": "AE Interactive 工作室",
    },
    "zh-Hans": {
        "html_lang": "zh-Hans",
        "title": "KoreanGo — 韩国旅游韩语、100 个实景对话视频、互动口语与双向语音翻译",
        "desc": "从 40 个韩文字母笔顺、24 组送气音与紧音辨音、100 个首尔旅游实景对话视频，到 12 情景互动口语与简中／韩语双向实时语音口译，无需登录零追踪。",
        "keywords": "KoreanGo,韩语学习,韩国旅游韩语,首尔自由行韩语,四十音,韩语紧音送气音,韩国实景对话,即时韩文翻译,AE Interactive",
        "nav_privacy": "隐私政策",
        "nav_support": "支持与常见问题",
        "nav_download": "立即下载" if APP_STORE_URL else "查看方案",
        "hero_badge": "15 节实战课 · 100 个首尔实景对话 · 双向语音翻译 · 零广告追踪",
        "hero_title": "落地仁川前，<span>先开口说出地道首尔旅游韩语</span>",
        "hero_sub": "从 40 个韩文字母描红与 24 组平音／送气音／紧音辨音起步，衔接 100 个首尔实景视频、店员主动提问模拟与现场双向实时口译——全程免注册、无广告。",
        "status_pill": (
            "App Store 正式上线 · 免费下载体验 · iPhone、iPad & iPhone Duo"
            if APP_STORE_URL
            else "专为 iPhone & iPad 原生打造 · iOS 17+ · 基础免费学"
        ),
        "cta_store_sub": "前往免费下载",
        "cta_store_main": "App Store",
        "cta_coming_main": "即将上线 · App Store",
        "cta_audio": "▶ 试听原生发音",
        "cta_screens": "查看实机截图 ↓",
        "cta_plans": "查看免费与 $3.99 Pro ↓",
        "sec_audio_badge": "内置录音室真人发音 · 连音与紧音标注",
        "sec_audio_title": "点击试听真实韩国旅游高频句",
        "sec_audio_sub": "直接试听 KoreanGo 应用内 693 句高清语音之一——掌握韩语紧音（ㄸ）、连音（갈아타요）与自然语调。",
        "btn_play": "播放",
        "btn_playing": "播放中",
        "sec_screens_badge": "实机界面展示 · IPHONE 6.9\" 与 IPAD 13\"",
        "sec_screens_title": "单手竖屏大字体，地铁站内一眼看清",
        "sec_screens_sub": "专为韩国自由行单手操作设计，支持三档大字号切换，并全面适配 iPad 13 英寸高清分栏展示。",
        "screens_labels": [
            "15 节实战路线",
            "12 情景实战互动对话",
            "首尔现场 · 双向语音翻译",
            "100 个首尔旅游实景对话",
            "40 字母笔顺与 24 组辨音",
            "iPad 13 英寸大屏视图",
        ],
        "sec_features_badge": "六大核心模块",
        "sec_features_title": "从韩文字母到现场应急，一站全搞定",
        "features": [
            ("📚", "15 节系统路线 + 18 节语法特训", "从元音、辅音与收音（Batchim）起步，系统覆盖烤肉店点单、美妆即时退税、首尔地铁换乘、酒店入住与看诊求助。"),
            ("🎬", "100 个首尔旅游实景对话视频（200 句音频）", "五大韩国旅游场景按行程阶段编排，包含完整首尔音标 IPA、罗马音、实用语法提示与三语对照。"),
            ("💬", "12 情景实战互动对话 + 自由表达", "采用端侧互动引导：由韩国店员先开口提问，跟读作答时全程保留提示卡片，陪你打通 3 关任务。"),
            ("🗣️", "双向实时语音翻译（底部栏最右一键直达）", "支持简中／繁中／英语／日语／西语 ↔ 韩语语音与文字即时互译，并附全屏大字卡片方便直接给店员看。"),
            ("✍️", "40 字母笔顺画板、24 组辨音与 160 SRS 词卡", "交互式书写描红、平音／送气音／紧音盲听分辨、693 句高清词句音频与三档大字体选项。"),
            ("🔒", "免账号登录 · 100% 本地隐私", "零广告、零第三方追踪代码（NSPrivacyTracking = false），学习进度仅保存于您的设备本地。"),
        ],
        "sec_pricing_badge": "无月费订阅 · 免费学基础再买断",
        "sec_pricing_title": "基础免费使用 · $3.99 一次永久买断",
        "sec_pricing_sub": "免费完整掌握 40 个韩文字母、24 组三类对立音与前 3 节课程，满意后再单次买断解锁全套 100 支短片与无限口译。",
        "free_tier_tag": "KOREANGO 免费版",
        "free_tier_title": "永久免费版",
        "free_tier_price": "免费 $0",
        "free_tier_items": [
            "完整 40 字韩文字母图表、双速发音与手写描红",
            "完整 24 组平音／送气音／紧音最小对立对听力挑战",
            "完整 160 核心词卡 SM-2 记忆与 4 大听力测验",
            "前 3 节课程 ＋ 10 支实景视频 ＋ 每日口语(5次)与口译(8次)",
        ],
        "pro_tier_badge": "一次买断 · 无订阅自动扣费",
        "pro_tier_title": "KoreanGo Pro 永久买断",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "解锁全部 15 节首尔自由行实战课程（第 4–15 节）",
            "解锁全部 100 部实景对话视频与 200 句真人录音",
            "12 大旅游情景店员互动口语及自由对话不限次数",
            "双向实时语音口译无限次使用（支持离线翻译包）",
        ],
        "bottom_cta_title": "下一趟韩国之旅，打开就能用",
        "bottom_cta_sub": "iPhone & iPad 原生体验・无需注册账号，出行前练好第一句地道韩语。",
        "appstore_btn_label": "前往 App Store 免费下载" if APP_STORE_URL else "查看完整免费功能 ↑",
        "coming_soon_btn": "即将上线 App Store · 技术支持",
        "privacy_title": "KoreanGo 隐私政策",
        "privacy_updated": "最后更新日期：2026 年 11 月 23 日",
        "privacy_sections": [
            ("1. 无需账号且不收集个人数据", "KoreanGo 由 AE Interactive（AppEngine Interactive）开发。本应用无需注册账号，不会向开发商服务器收集、存储、出售或传输任何个人身份信息（App Store Privacy 声明“不收集数据”，NSPrivacyTracking = false）。学习记录、词卡复习与字号设置仅通过系统 UserDefaults（Required Reason API CA92.1）保存在设备本地。"),
            ("2. 麦克风、语音识别与端侧对话处理", "仅在您主动点击“互动口语练习”或“双向实时口译”中的麦克风按钮时才申请权限；语音识别（ko-KR）、Apple 本地翻译与端侧对话框架均优先在设备端运行，不会将对话发送至第三方服务器。"),
            ("3. 零广告与零第三方追踪", "本应用不含任何广告 SDK、第三方数据统计或跨应用追踪。"),
            ("4. 联系我们", "如有隐私相关咨询，请联系 help@appengine.fun。"),
        ],
        "support_title": "技术支持与常见问题 — KoreanGo",
        "support_sub": "互动口语兼容说明、韩语离线翻译包下载及联系客服。",
        "support_cards": [
            ("互动口语支持机型", "基于 Apple 原生端侧系统语言框架运行，支持 iPhone 15 Pro / Pro Max、iPhone 16 / 17 系列及更新机型或 M 系列 / A17 Pro 以上 iPad（iOS / iPadOS 26.0+ 并开启相应系统功能），并在全部 iOS 17+ 机型提供本地短语指引支持。"),
            ("全部课程、100 部实景视频与 693 句音频无机型门槛", "15 节课程、40 字母描红、24 组辨音、100 个首尔旅游实景视频、160 词卡与 18 节语法在全部兼容 iOS 17.0+ 设备上免登录即可离线使用。"),
            ("出行前建议预载韩语离线翻译包", "“双向实时语音翻译”使用 Apple 系统 Translation 框架；可在系统“设置 → App → 翻译”预载“简体中文 ↔ 韩语”离线包，机场或地下站台没信号也能顺畅沟通。"),
            ("联系技术支持", "如需帮助请致信 help@appengine.fun，AE Interactive 团队通常于 24 小时内回复。"),
        ],
        "footer_rights": "© 2026 AE Interactive. 保留所有权利。",
        "studio_link_label": "AE Interactive 工作室",
    },
    "ja": {
        "html_lang": "ja",
        "title": "KoreanGo — 旅行韓国語・ソウル実境会話動画100本・音声練習・双方向通訳",
        "desc": "ハングル40文字の書き順と3系列聞き分け24組から、ソウル実境会話動画100本・12場面ロールプレイ・リアルタイム双方向音声通訳まで1つで完結。",
        "keywords": "KoreanGo,旅行韓国語,ハングル,韓国語聞き分け,韓国旅行会話,リアルタイム韓国語翻訳,AE Interactive",
        "nav_privacy": "プライバシー",
        "nav_support": "サポート",
        "nav_download": "入手する" if APP_STORE_URL else "料金を見る",
        "hero_badge": "全15課 · ソウル実境会話動画100本 · 双方向通訳 · 広告ゼロ",
        "hero_title": "仁川に着く前に、<br><span>そのまま使える韓国語を口に</span>",
        "hero_sub": "ハングル40文字の書き順・平音/激音/濃音の聞き分け24組・ソウル実境動画100本から、12場面ロールプレイとリアルタイム双方向音声通訳まで。アカウント登録も広告も一切なし。",
        "status_pill": (
            "App Store 配信中 · 無料スタート · iPhone・iPad・iPhone Duo 対応"
            if APP_STORE_URL
            else "iPhone & iPad ネイティブ設計 · iOS 17+ · 基礎無料で体験"
        ),
        "cta_store_sub": "無料で入手",
        "cta_store_main": "App Store",
        "cta_coming_main": "App Store 公開準備中",
        "cta_audio": "▶ ネイティブ音声を試聴",
        "cta_screens": "画面プレビュー ↓",
        "cta_plans": "無料プランと $3.99 Pro ↓",
        "sec_audio_badge": "アプリ収録ネイティブ音声 · 発音変化＆ローマ字表記",
        "sec_audio_title": "現地でそのまま聞こえるリアルな発音",
        "sec_audio_sub": "KoreanGo に収録された693本のスタジオ音声から一部を試聴—濃音（ㄸ）や連音化（갈아타요）も自然に身につきます。",
        "btn_play": "再生",
        "btn_playing": "再生中",
        "sec_screens_badge": "実機画面プレビュー · IPHONE 6.9\" & IPAD 13\"",
        "sec_screens_title": "片手で迷わず読める旅行特化デザイン",
        "sec_screens_sub": "移動中の地下鉄ホームでも見やすい縦型大文字設計。標準・大・特大の3段階フォントサイズと iPad 13インチ大画面に最適化。",
        "screens_labels": [
            "全15課の学習ルート",
            "12場面の実践音声練習",
            "現地で使える双方向通訳",
            "100本のソウル会話動画",
            "40文字＆24組聞き分け",
            "iPad 13インチ大画面対応",
        ],
        "sec_features_badge": "6つの統合モジュール",
        "sec_features_title": "オフライン対応・これ1つで韓国旅行も安心",
        "features": [
            ("📚", "全15課＋文法ドリル18問", "ハングルの母音・子音・パッチムから、カフェやサムギョプサル注文、オリーブヤング免税、地下鉄2号線乗り換え、ホテルや緊急対応まで段階的に習得。"),
            ("🎬", "ソウル実境会話動画 100本（音声200収録）", "5大シチュエーション別の実践動画を収録。ソウル標準IPA音標・ローマ字表記・解説ポイント付きで自然に聞き取れます。"),
            ("💬", "12場面の実践ロールプレイ＋フリートーク", "現地スタッフの一言からスタートし、画面上のヒントを見ながら声に出して3ステップの会話ミッションをクリア。"),
            ("🗣️", "リアルタイム双方向音声通訳（右端タブで即起動）", "日本語・英語・中国語・スペイン語 ⇄ 韓国語の音声・テキスト双方向翻訳に対応。店員にそのまま見せる全画面カード表示付き。"),
            ("✍️", "ハングル40文字筆順・24組聞き分け・160語SRS", "書き順トレースキャンバス、平音・激音・濃音の3系列ブラインド練習、693本のネイティブ音声、文字サイズ3段階調節を内蔵。"),
            ("🔒", "ログイン不要・完全オンデバイス設計", "広告SDKやトラッキングは一切なし（NSPrivacyTracking = false）。学習データはすべて端末内の UserDefaults のみに保存されます。"),
        ],
        "sec_pricing_badge": "月額課金なし · 無料で基礎マスター",
        "sec_pricing_title": "基礎は無料。$3.99 一度きりの買い切り",
        "sec_pricing_sub": "ハングル40文字と24組聞き分け、1〜3課を無料で試したあと、全100本の動画や通訳無制限が必要になった時点で1回だけ解放できます。",
        "free_tier_tag": "KOREANGO 無料プラン",
        "free_tier_title": "ずっと無料",
        "free_tier_price": "$0",
        "free_tier_items": [
            "全40ハングル一覧＆筆順トレーニングキャンバス",
            "全24組の平音・激音・濃音 聞き分けドリル",
            "全160語 SM-2 単語カード＆4種類のクイズ形式",
            "レッスン1〜3 ＋ 動画10本 ＋ 毎日の音声練習(5回/日)・通訳(8回/日)",
        ],
        "pro_tier_badge": "一度きりの買い切り · サブスクなし",
        "pro_tier_title": "KoreanGo Pro 永久アンロック",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "全15課の旅行実践コースを完全解放（4〜15課）",
            "全100本のソウル会話動画＆200本のネイティブ録音",
            "12場面の実践音声練習＆フリートーク回数無制限",
            "双方向リアルタイム音声通訳を無制限利用（オフライン対応）",
        ],
        "bottom_cta_title": "次のソウル旅行は、これ1つで準備完了",
        "bottom_cta_sub": "iPhone & iPad 対応・登録不要・オフラインでもすぐに韓国語を練習できます。",
        "appstore_btn_label": "App Store で無料入手" if APP_STORE_URL else "無料プランの内容を確認 ↑",
        "coming_soon_btn": "v1.0 リリース準備中・お問い合わせ",
        "privacy_title": "プライバシーポリシー — KoreanGo",
        "privacy_updated": "最終更新日：2026年11月23日",
        "privacy_sections": [
            ("1. アカウント登録なし・個人データ不収集", "KoreanGo は AE Interactive（AppEngine Interactive）が開発しています。アカウント登録は不要で、開発者サーバーへ個人情報を収集・保存・販売・送信することは一切ありません（App Store Privacy：データ収集なし / NSPrivacyTracking = false）。学習進捗や文字サイズ設定は端末内の Apple UserDefaults（CA92.1）にのみ保存されます。"),
            ("2. マイク・音声認識・オンデバイス処理", "マイクおよび音声認識（ko-KR）の許可は、音声練習または通訳タブで録音ボタンを押した時にのみ要求されます。翻訳や会話アシストは Apple ネイティブのオンデバイスフレームワークを優先利用します。"),
            ("3. 広告・トラッキング一切なし", "広告ネットワーク、第三者アナリティクスSDK、クロスアプリ追跡は一切組み込まれていません。"),
            ("4. お問い合わせ", "ご質問は help@appengine.fun までお気軽にご連絡ください。"),
        ],
        "support_title": "サポート＆対応環境 — KoreanGo",
        "support_sub": "音声ロールプレイの対応機種、オフライン翻訳パック設定、サポート窓口のご案内。",
        "support_cards": [
            ("音声ロールプレイ対応機種", "Apple のオンデバイスシステム言語フレームワークに対応した端末（iPhone 15 Pro / Pro Max、iPhone 16 / 17 シリーズ以降、Mシリーズ / A17 Pro以降のiPad、iOS / iPadOS 26.0+ 推奨）でフル動作し、すべての iOS 17+ 端末でもフレーズ判定サポートを利用できます。"),
            ("オフライン学習・動画100本・音声693本は全機種対応", "全15課、ハングル40文字筆順、聞き分け24組、単語帳160語、文法18問、実境動画100本はログイン不要で iOS 17.0 以降のすべての対応 iPhone / iPad でご利用いただけます。"),
            ("渡航前の韓国語オフライン翻訳パック設定", "双方向音声通訳は Apple 純正の Translation フレームワークを使用します。ご出発前に iOS「設定 → アプリ → 翻訳」から「日本語 ⇄ 韓国語」パックをダウンロードしておくと電波が弱い場所でも安心です。"),
            ("直接サポート窓口", "お困りの点やご要望は help@appengine.fun までお送りください（通常24時間以内に返信いたします）。"),
        ],
        "footer_rights": "© 2026 AE Interactive. All rights reserved.",
        "studio_link_label": "AE Interactive スタジオ",
    },
    "es": {
        "html_lang": "es",
        "title": "KoreanGo — Coreano de Viaje, 100 Vídeos Reales, Práctica Oral y Traducción",
        "desc": "Aprende coreano práctico para viajar a Seúl con 40 Hangul Jamo con trazos, 24 pares mínimos, 100 vídeos reales en Corea, Práctica Oral en 12 escenarios e Intérprete en Vivo.",
        "keywords": "KoreanGo,coreano viaje,hangul,corea,seul,pares minimos coreano,traductor coreano voz,AE Interactive",
        "nav_privacy": "Privacidad",
        "nav_support": "Soporte",
        "nav_download": "Descargar" if APP_STORE_URL else "Ver Planes",
        "hero_badge": "15 LECCIONES · 100 VÍDEOS EN SEÚL · TRADUCCIÓN EN VIVO · SIN ANUNCIOS",
        "hero_title": "Habla Coreano Real<br><span>Antes de Aterrizar en Seúl</span>",
        "hero_sub": "Desde las 40 letras Hangul con trazos y 24 pares mínimos hasta 100 vídeos reales en Corea, Práctica Oral guiada en 12 escenarios e Intérprete Bidireccional en Vivo—sin cuentas ni rastreo.",
        "status_pill": (
            "Disponible en App Store · Gratis para empezar · iPhone, iPad e iPhone Duo"
            if APP_STORE_URL
            else "App nativa iPhone & iPad · iOS 17+ · Empieza gratis sin cuenta"
        ),
        "cta_store_sub": "Descárgalo gratis en",
        "cta_store_main": "App Store",
        "cta_coming_main": "En Revisión App Store",
        "cta_audio": "▶ Escuchar Audio Real",
        "cta_screens": "Ver Capturas ↓",
        "cta_plans": "Ver Plan Gratis y Pro ($3.99) ↓",
        "sec_audio_badge": "AUDIO DE ESTUDIO REAL · ROMANIZACIÓN E IPA CLAROS",
        "sec_audio_title": "Escucha Coreano Real Antes de Tu Viaje",
        "sec_audio_sub": "Audios MP3 incluidos dentro de KoreanGo (693 grabaciones en total) para dominar consonantes tensas (ㄸ) y ligaduras de Seúl.",
        "btn_play": "Reproducir",
        "btn_playing": "Sonando",
        "sec_screens_badge": "CAPTURAS REALES DE LA APP · IPHONE 6.9\" E IPAD 13\"",
        "sec_screens_title": "Diseñada para Leer Cómodo a Una Mano",
        "sec_screens_sub": "Diseñada para leer rápido en cafeterías o en el metro de Seúl, con tamaño de letra Normal / Grande / Extra e iPad 13\" adaptado.",
        "screens_labels": [
            "Ruta de 15 Lecciones",
            "Práctica en 12 Escenarios",
            "Intérprete en Vivo",
            "100 Vídeos en Corea",
            "40 Hangul y Pares",
            "Pantalla iPad 13\"",
        ],
        "sec_features_badge": "SEIS MÓDULOS INTEGRADOS",
        "sec_features_title": "Todo en Una App Privada y Lista Sin Internet",
        "features": [
            ("📚", "15 Unidades Prácticas y 18 Ejercicios", "Domina las 40 letras Hangul y sus consonantes finales hasta pedir en barbacoas, tiendas Tax-Free, metro Línea 2, hoteles y emergencias."),
            ("🎬", "100 Vídeos de Diálogos Reales en Seúl", "Organizados en 5 categorías reales de viaje con 200 audios de estudio, subtítulos bilingües, romanización revisada e IPA."),
            ("💬", "Práctica Oral Guiada en 12 Escenarios", "Tu interlocutor inicia la conversación y mantiene tus tarjetas de ayuda visibles mientras hablas para completar cada misión."),
            ("🗣️", "Intérprete Bidireccional en Vivo", "Habla o escribe en Español, Inglés, Japonés o Chino al instante con coreano, con lectura automática y tarjeta a pantalla completa."),
            ("✍️", "40 Hangul, 24 Pares Mínimos y 160 Tarjetas SRS", "Lienzo de trazos letra a letra, test auditivos a ciegas entre suave/aspirada/tensa, 693 grabaciones y tamaño de fuente ajustable."),
            ("🔒", "Sin Registro · Privacidad Total en el Dispositivo", "Sin cuentas, sin anuncios ni SDKs de rastreo (NSPrivacyTracking = false). Todo tu avance permanece exclusivamente en tu dispositivo."),
        ],
        "sec_pricing_badge": "SIN SUSCRIPCIONES · EMPIEZA GRATIS",
        "sec_pricing_title": "Gratis para Empezar. $3.99 Pago Único.",
        "sec_pricing_sub": "Empieza gratis con Hangul, 24 pares mínimos y 160 tarjetas, y desbloquea los 100 vídeos e intérprete ilimitado cuando quieras con un único pago.",
        "free_tier_tag": "KOREANGO GRATIS",
        "free_tier_title": "Gratis para Siempre",
        "free_tier_price": "$0",
        "free_tier_items": [
            "Las 40 letras Hangul y lienzo interactivo de trazos",
            "Los 24 pares mínimos (suave / aspirada / tensa y batchim)",
            "Las 160 tarjetas SM-2 y los 4 modos de test interactivo",
            "Unidades 1–3 + 10 vídeos reales + cuota diaria de voz (5/día) e intérprete (8/día)",
        ],
        "pro_tier_badge": "PAGO ÚNICO · SIN SUSCRIPCIÓN",
        "pro_tier_title": "KoreanGo Pro De Por Vida",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "Las 15 unidades guiadas de viaje (4–15 desbloqueadas)",
            "Los 100 vídeos de diálogo real en Corea y 200 audios nativos",
            "Práctica Oral ilimitada en 12 escenarios + charla libre",
            "Intérprete Bidireccional en Vivo sin límites (con modo offline)",
        ],
        "bottom_cta_title": "Aterriza en Incheon Listo para Hablar Coreano",
        "bottom_cta_sub": "Creada para iPhone e iPad — aprende a tu ritmo sin cuenta y sin suscripciones.",
        "appstore_btn_label": "Descargar gratis en App Store" if APP_STORE_URL else "Ver qué incluye gratis ↑",
        "coming_soon_btn": "v1.0.0 Muy Pronto · Contacto",
        "privacy_title": "Política de Privacidad — KoreanGo",
        "privacy_updated": "Última actualización: 23 de noviembre de 2026",
        "privacy_sections": [
            ("1. Sin Cuenta y Sin Recopilación de Datos", "KoreanGo es desarrollada por AE Interactive (AppEngine Interactive). No exige registro de cuenta ni recopila, vende o envía datos personales a servidores propios (Etiqueta App Store: No se recopilan datos / NSPrivacyTracking = false). Todo tu avance de aprendizaje y preferencias locales se guardan únicamente en tu dispositivo mediante Apple UserDefaults (CA92.1)."),
            ("2. Micrófono, Reconocimiento de Voz y Procesamiento Local", "El micrófono y el reconocimiento de voz (ko-KR) solo se solicitan cuando pulsas el botón de grabación en la Práctica Oral o el Intérprete en Vivo. La traducción y las respuestas se ejecutan en el dispositivo con marcos nativos de Apple."),
            ("3. Sin Publicidad ni Rastreo", "KoreanGo no incluye redes publicitarias, analítica de terceros ni seguimiento entre apps."),
            ("4. Contacto", "Para consultas de privacidad o soporte, escribe a help@appengine.fun."),
        ],
        "support_title": "Soporte y Compatibilidad — KoreanGo",
        "support_sub": "Requisitos de Práctica Oral en el dispositivo, paquetes de traducción offline y contacto directo.",
        "support_cards": [
            ("Compatibilidad de la Práctica Oral", "Funciona localmente con el modelo de lenguaje del sistema de Apple en iPhone 15 Pro / Pro Max, iPhone 16 / 17 o posterior y iPad con M1 / A17 Pro+ con iOS / iPadOS 26.0+. En todos los iPhone/iPad compatibles con iOS 17+ sigue disponible la práctica guiada."),
            ("100 Vídeos, 40 Hangul y 693 Audios en Cualquier Dispositivo", "Las 15 unidades, los 40 Hangul con trazos, 24 pares mínimos, 160 tarjetas SRS, 18 ejercicios de gramática y los 100 vídeos funcionan totalmente offline desde iOS 17.0 sin cuenta."),
            ("Paquete Offline de Coreano en iOS", "El Intérprete Bidireccional en Vivo usa Apple Translation. Antes de viajar, ve a Ajustes de iOS → Apps → Traducir y descarga Español ⇄ Coreano para traducir sin cobertura."),
            ("Soporte Directo", "¿Dudas, sugerencias o errores? Escríbenos a help@appengine.fun y respondemos habitualmente en menos de 24 horas."),
        ],
        "footer_rights": "© 2026 AE Interactive. Todos los derechos reservados.",
        "studio_link_label": "Estudio AE Interactive",
    },
}

AUDIO_ITEMS = [
    {
        "file": "split.mp3",
        "ko": "두 명 따로 계산해도 돼요?",
        "roman": "Du myeong <b>ttaro</b> gyesanhaedo dwaeyo?",
        "ipa": "[tu mjʌŋ t͈a.ɾo kje.san.ɦɛ.do twɛ.jo]",
        "meaning": {
            "en": "Can the two of us pay separately?",
            "zh-Hant": "請問兩個人分開結帳可以嗎？",
            "zh-Hans": "请问两个人分开结账可以吗？",
            "ja": "2人別々にお会計してもいいですか？",
            "es": "¿Podemos pagar los dos por separado?",
        },
        "tag": {
            "en": "Dining · Tense Consonant tt (따)",
            "zh-Hant": "餐廳分帳 · 緊音 ㄸ (따로)",
            "zh-Hans": "餐厅分账 · 紧音 ㄸ (따로)",
            "ja": "レストラン · 濃音 ㄸ (따로)",
            "es": "Restaurante · Consonante tensa ㄸ",
        },
    },
    {
        "file": "transfer.mp3",
        "ko": "어느 역에서 2호선으로 갈아타요?",
        "roman": "Eoneu yeogeseo ihoseoneuro <b>gara</b>tayo?",
        "ipa": "[ʌ.nɯ jʌ.ɡe.sʌ i.ɦo.sʌ.nɯ.ɾo ka.ɾa.tʰa.jo]",
        "meaning": {
            "en": "Which station do I transfer to Line 2 at?",
            "zh-Hant": "請問在哪一站轉乘二號線呢？",
            "zh-Hans": "请问在哪一站换乘二号线呢？",
            "ja": "どの駅で2号線に乗り換えますか？",
            "es": "¿En qué estación hago transbordo a la línea 2?",
        },
        "tag": {
            "en": "Seoul Metro · Liaison ㄹ -> r",
            "zh-Hant": "首爾地鐵 · 連音變化 갈아타요",
            "zh-Hans": "首尔地铁 · 连音变化 갈아타요",
            "ja": "ソウル地下鉄 · 連音化 갈아타요",
            "es": "Metro de Seúl · Ligadura ㄹ -> r",
        },
    },
    {
        "file": "checkout.mp3",
        "ko": "체크아웃 시간이 몇 시예요?",
        "roman": "Chekeuaut sigani <b>myeot ssi</b>yeyo?",
        "ipa": "[tɕʰe.kʰɯ.a.ut ɕi.ɡa.ni mjʌt ɕ͈i.je.jo]",
        "meaning": {
            "en": "What time is check-out?",
            "zh-Hant": "請問退房時間是幾點？",
            "zh-Hans": "请问退房时间是几点？",
            "ja": "チェックアウトは何時ですか？",
            "es": "¿A qué hora es el check-out?",
        },
        "tag": {
            "en": "Hotel Desk · Time Counter & Tensification",
            "zh-Hant": "飯店櫃檯 · 時間說法與音變",
            "zh-Hans": "酒店前台 · 时间问法与音变",
            "ja": "ホテル受付 · 時刻表現＆濃音化",
            "es": "Recepción · Horas y tensificación",
        },
    },
    {
        "file": "slowly.mp3",
        "ko": "조금만 천천히 말씀해 주세요.",
        "roman": "Jogeumman <b>cheoncheoni</b> malsseumhae juseyo.",
        "ipa": "[tɕo.ɡɯm.man tɕʰʌn.tɕʰʌ.ni mal.s͈ɯm.ɦɛ tɕu.se.jo]",
        "meaning": {
            "en": "Please speak just a little more slowly.",
            "zh-Hant": "麻煩請再說慢一點點。",
            "zh-Hans": "麻烦请再说慢一点点。",
            "ja": "もう少しゆっくり話してください。",
            "es": "Por favor, hable un poco más despacio.",
        },
        "tag": {
            "en": "Polite Rescue · Soft Medial ㅎ",
            "zh-Hant": "禮貌必備句 · 弱化音 ㅎ",
            "zh-Hans": "礼貌救援句 · 弱化音 ㅎ",
            "ja": "必須フレーズ · 弱音化 ㅎ",
            "es": "Frase clave · Debilitación de ㅎ",
        },
    },
]

CSS = """
:root {
  --bg: #070913;
  --card: rgba(20, 24, 42, 0.86);
  --card-solid: #14182a;
  --border: rgba(255, 255, 255, 0.11);
  --text: #F8FAFC;
  --muted: #94A3B8;
  --indigo: #6366F1;
  --teal: #2DD4BF;
  --coral: #FB7185;
}
* { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
html { scroll-behavior: smooth; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Apple SD Gothic Neo", "PingFang TC", "PingFang SC", "Hiragino Sans", "Helvetica Neue", Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  overflow-x: hidden;
  background-image:
    radial-gradient(ellipse 80% 42% at 50% -5%, rgba(99, 102, 241, 0.24) 0%, transparent 70%),
    radial-gradient(circle at 86% 18%, rgba(45, 212, 191, 0.14) 0%, transparent 45%);
  background-repeat: no-repeat;
}
a { color: inherit; }
header { position: sticky; top: 12px; z-index: 100; padding: 0 16px; }
nav {
  max-width: 980px; margin: 0 auto; padding: 10px 16px;
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
  background: rgba(11, 14, 28, 0.84);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border); border-radius: 999px;
  box-shadow: 0 12px 34px rgba(0,0,0,0.45);
}
.brand { display: flex; align-items: center; gap: 10px; text-decoration: none; font-weight: 800; font-size: 17px; letter-spacing: -0.3px; }
.brand img { width: 34px; height: 34px; border-radius: 9px; border: 1px solid rgba(45, 212, 191, 0.45); }
.nav-right { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.nav-links { display: flex; gap: 14px; font-size: 13px; font-weight: 600; color: var(--muted); }
.nav-links a { text-decoration: none; transition: color .18s; }
.nav-links a:hover, .nav-links a.active { color: #fff; }
.lang-picker {
  display: flex; align-items: center; gap: 4px;
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.09);
  padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700;
}
.lang-picker a { color: var(--muted); text-decoration: none; padding: 2px 5px; border-radius: 99px; }
.lang-picker a.active { color: var(--teal); background: rgba(45,212,191,0.14); }
main { max-width: 980px; margin: 0 auto; padding: 36px 18px 64px; }
.hero { text-align: center; padding: 20px 0 36px; }
.badge {
  display: inline-block; font-size: 11px; font-weight: 800; letter-spacing: 0.7px;
  color: var(--teal); background: rgba(45,212,191,0.12);
  border: 1px solid rgba(45,212,191,0.34); padding: 6px 14px; border-radius: 999px; margin-bottom: 16px;
}
h1 { font-size: clamp(30px, 5.4vw, 54px); font-weight: 900; letter-spacing: -1.1px; line-height: 1.12; margin-bottom: 14px; text-wrap: balance; }
h1 span { background: linear-gradient(125deg, #818CF8 0%, #2DD4BF 62%, #FB7185 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { max-width: 680px; margin: 0 auto 22px; color: var(--muted); font-size: clamp(15px, 2vw, 18px); text-wrap: balance; }
.status-pill {
  display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 999px;
  background: rgba(99,102,241,0.14); border: 1px solid rgba(99,102,241,0.38);
  color: #C7D2FE; font-size: 13px; font-weight: 700; margin-bottom: 22px;
}
.hero-cta { display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }
.btn {
  display: inline-flex; align-items: center; gap: 8px; padding: 12px 22px; border-radius: 999px;
  font-size: 14px; font-weight: 700; text-decoration: none; border: 1px solid transparent; cursor: pointer;
  transition: transform .16s ease, box-shadow .16s ease, background .16s ease;
}
.btn:hover { transform: translateY(-1px); }
.btn-primary { background: linear-gradient(135deg, #6366F1, #14B8A6); color: #fff; box-shadow: 0 10px 26px rgba(99,102,241,0.32); }
.btn-ghost { background: rgba(255,255,255,0.06); border-color: var(--border); color: #E2E8F0; }
.btn-appstore {
  background: #fff; color: #090D16; border: 1px solid rgba(255,255,255,0.85);
  padding: 9px 20px; gap: 10px; box-shadow: 0 12px 30px rgba(255,255,255,0.16), 0 8px 24px rgba(99,102,241,0.28);
}
.btn-appstore svg { width: 20px; height: 24px; fill: currentColor; flex-shrink: 0; }
.btn-appstore .as-copy { display: flex; flex-direction: column; align-items: flex-start; line-height: 1.12; text-align: left; }
.btn-appstore .as-sub { font-size: 10px; font-weight: 700; opacity: 0.72; letter-spacing: 0.2px; }
.btn-appstore .as-main { font-size: 15px; font-weight: 850; letter-spacing: -0.2px; }
.nav-cta {
  display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 999px;
  background: linear-gradient(135deg, #6366F1, #14B8A6); color: #fff; text-decoration: none;
  font-size: 12.5px; font-weight: 800; box-shadow: 0 4px 14px rgba(99,102,241,0.35);
  transition: transform .16s ease, filter .16s ease;
}
.nav-cta:hover { transform: translateY(-1px); filter: brightness(1.08); }
.pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 16px; }
.price-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 22px; padding: 24px;
  display: flex; flex-direction: column; justify-content: space-between; gap: 18px;
}
.price-card.pro {
  border-color: rgba(45, 212, 191, 0.55);
  background: linear-gradient(160deg, rgba(99,102,241,0.16), rgba(20,24,42,0.94) 45%, rgba(20,184,166,0.14));
  box-shadow: 0 18px 40px rgba(0,0,0,0.42);
}
.price-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
.price-tag { font-size: 11px; font-weight: 800; color: var(--teal); letter-spacing: 0.4px; margin-bottom: 4px; }
.price-title { font-size: 20px; font-weight: 850; color: #fff; }
.price-num { font-size: 26px; font-weight: 900; color: #fff; white-space: nowrap; }
.price-list { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.price-list li { display: flex; gap: 9px; font-size: 14px; color: #CBD5E1; line-height: 1.45; }
.price-list li span.chk { color: var(--teal); font-weight: 900; flex-shrink: 0; }
.price-card .btn-appstore { justify-content: center; }
.cta-banner {
  margin-top: 56px; padding: 34px 24px; border-radius: 26px; text-align: center;
  background: linear-gradient(135deg, rgba(99,102,241,0.22), rgba(20,184,166,0.18));
  border: 1px solid rgba(45,212,191,0.35);
  display: flex; flex-direction: column; align-items: center; gap: 14px;
}
.cta-banner img { width: 64px; height: 64px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.25); box-shadow: 0 10px 28px rgba(0,0,0,0.4); }
.cta-banner h2 { margin-bottom: 0; }
.cta-banner p { color: #CBD5E1; max-width: 540px; font-size: 15px; }
section { margin-top: 56px; }
.sec-head { text-align: center; margin-bottom: 24px; }
.sec-head .badge { margin-bottom: 10px; }
h2 { font-size: clamp(22px, 3.6vw, 34px); font-weight: 850; letter-spacing: -0.6px; margin-bottom: 8px; }
.sec-sub { color: var(--muted); max-width: 620px; margin: 0 auto; font-size: 15px; }
.audio-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }
.audio-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 18px; padding: 16px;
  display: flex; flex-direction: column; justify-content: space-between; gap: 12px;
  transition: border-color .2s, transform .2s;
}
.audio-card.playing { border-color: var(--teal); box-shadow: 0 0 0 1px rgba(45,212,191,0.3), 0 14px 32px rgba(0,0,0,0.4); }
.audio-tag { font-size: 11px; font-weight: 700; color: var(--teal); letter-spacing: 0.3px; }
.audio-ko { font-size: 18px; font-weight: 800; margin-top: 6px; color: #fff; }
.audio-roman { font-size: 13px; color: #67E8F9; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; margin-top: 4px; }
.audio-roman b { background: rgba(251, 113, 133, 0.2); color: #FDA4AF; padding: 0 4px; border-radius: 4px; }
.audio-ipa { font-size: 12px; color: #94A3B8; font-family: "Charis SIL", "Doulos SIL", "Lucida Grande", "Segoe UI", "Arial Unicode MS", "DejaVu Sans", sans-serif; margin-top: 2px; letter-spacing: 0.2px; }
.audio-meaning { font-size: 13px; color: var(--muted); margin-top: 5px; }
.play-btn {
  align-self: flex-start; background: rgba(99,102,241,0.2); color: #C7D2FE; border: 1px solid rgba(99,102,241,0.4);
  padding: 6px 14px; border-radius: 999px; font-size: 12.5px; font-weight: 700; cursor: pointer;
}
.audio-card.playing .play-btn { background: var(--teal); color: #042F2E; border-color: var(--teal); }
.gallery-strip {
  display: flex; gap: 16px; overflow-x: auto; padding: 8px 4px 16px; scroll-snap-type: x mandatory;
}
.shot-card {
  flex: 0 0 230px; scroll-snap-align: start; background: var(--card); border: 1px solid var(--border);
  border-radius: 20px; padding: 10px; text-align: center;
}
.shot-card.wide { flex: 0 0 340px; }
.shot-card img { width: 100%; height: auto; border-radius: 14px; display: block; }
.shot-cap { font-size: 12.5px; font-weight: 700; color: #CBD5E1; margin-top: 9px; }
.bento { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }
.bento-card { background: var(--card); border: 1px solid var(--border); border-radius: 20px; padding: 20px; }
.bento-icon { font-size: 24px; margin-bottom: 10px; }
.bento-card h3 { font-size: 17px; font-weight: 800; margin-bottom: 6px; color: #fff; }
.bento-card p { font-size: 14px; color: var(--muted); }
.doc-box { max-width: 780px; margin: 14px auto; background: var(--card); border: 1px solid var(--border); border-radius: 22px; padding: 28px; }
.doc-box h1 { font-size: clamp(24px, 4vw, 36px); text-align: left; }
.doc-item { margin-top: 22px; padding-top: 18px; border-top: 1px solid var(--border); }
.doc-item h2 { font-size: 18px; margin-bottom: 6px; color: #E2E8F0; }
.doc-item p { font-size: 14.5px; color: var(--muted); }
footer {
  max-width: 980px; margin: 36px auto 0; padding: 24px 18px 42px;
  border-top: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap;
  color: var(--muted); font-size: 13px;
}
footer a { color: #CBD5E1; text-decoration: none; }
footer a:hover { color: var(--teal); }
@media (max-width: 680px) {
  nav { border-radius: 22px; padding: 10px 14px; }
  .nav-right { gap: 8px; }
  .hero-cta .btn { width: 100%; justify-content: center; max-width: 300px; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .btn, .audio-card { transition: none; }
}
"""

SCRIPT_JS = """
const audioMap = {};
let activeKey = null;
function togglePhrase(key, src, btnEl, cardEl, playLabel, playingLabel) {
  if (activeKey && activeKey !== key && audioMap[activeKey]) {
    audioMap[activeKey].audio.pause();
    audioMap[activeKey].audio.currentTime = 0;
    audioMap[activeKey].btn.textContent = "▶ " + playLabel;
    audioMap[activeKey].card.classList.remove("playing");
  }
  let item = audioMap[key];
  if (!item) {
    const a = new Audio(src);
    item = { audio: a, btn: btnEl, card: cardEl };
    a.addEventListener("ended", () => {
      btnEl.textContent = "▶ " + playLabel;
      cardEl.classList.remove("playing");
      if (activeKey === key) activeKey = null;
    });
    audioMap[key] = item;
  }
  if (!item.audio.paused) {
    item.audio.pause();
    item.audio.currentTime = 0;
    btnEl.textContent = "▶ " + playLabel;
    cardEl.classList.remove("playing");
    activeKey = null;
  } else {
    item.audio.play();
    btnEl.textContent = "■ " + playingLabel;
    cardEl.classList.add("playing");
    activeKey = key;
  }
}
"""


def appstore_badge_svg() -> str:
    return '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'


def nav_html(lang: str, route: str, t: dict) -> str:
    langs = [("en", "EN"), ("zh-Hant", "繁中"), ("zh-Hans", "简中"), ("ja", "日本語"), ("es", "ES")]
    lang_links = []
    for code, label in langs:
        cls = ' class="active"' if code == lang else ""
        href = f"{route}?lang={code}"
        lang_links.append(f'<a href="{href}"{cls}>{label}</a>')
    p_cls = ' class="active"' if route == "/privacy" else ""
    s_cls = ' class="active"' if route == "/support" else ""
    q = f"?lang={lang}"
    nav_cta_href = APP_STORE_URL if APP_STORE_URL else f"/{q}#pricing"
    nav_cta_attrs = ' target="_blank" rel="noopener noreferrer"' if APP_STORE_URL else ""
    return f"""
<header>
  <nav aria-label="Main navigation">
    <a class="brand" href="/{q}">
      <img src="/images/icon.webp" alt="KoreanGo Icon" width="34" height="34">
      <span>KoreanGo</span>
    </a>
    <div class="nav-right">
      <div class="nav-links">
        <a href="/privacy{q}"{p_cls}>{html_mod.escape(t['nav_privacy'])}</a>
        <a href="/support{q}"{s_cls}>{html_mod.escape(t['nav_support'])}</a>
      </div>
      <div class="lang-picker" role="navigation" aria-label="Language">{''.join(lang_links)}</div>
      <a class="nav-cta" href="{nav_cta_href}"{nav_cta_attrs}>{html_mod.escape(t['nav_download'])}</a>
    </div>
  </nav>
</header>"""


def footer_html(lang: str, t: dict) -> str:
    q = f"?lang={lang}"
    store_link = (
        f'<a href="{APP_STORE_URL}" target="_blank" rel="noopener noreferrer">App Store</a>'
        if APP_STORE_URL
        else ""
    )
    return f"""
<footer>
  <div>{html_mod.escape(t['footer_rights'])}</div>
  <div style="display:flex;gap:16px;flex-wrap:wrap;">
    <a href="/{q}">KoreanGo</a>
    {store_link}
    <a href="/privacy{q}">{html_mod.escape(t['nav_privacy'])}</a>
    <a href="/support{q}">{html_mod.escape(t['nav_support'])}</a>
    <a href="https://appengine.fun" target="_blank" rel="noopener noreferrer">{html_mod.escape(t['studio_link_label'])}</a>
    <a href="mailto:help@appengine.fun">help@appengine.fun</a>
  </div>
</footer>"""


OG_LOCALES = {
    "en": "en_US",
    "zh-Hant": "zh_TW",
    "zh-Hans": "zh_CN",
    "ja": "ja_JP",
    "ko": "ko_KR",
    "es": "es_ES",
}


def head_html(lang: str, t: dict, title: str, canonical_path: str, faq_items: list[tuple[str, str]] | None = None) -> str:
    q = f"?lang={lang}" if lang != "en" else ""
    canon_url = f"{ORIGIN}{canonical_path}{q}"
    site_langs = ('en', 'zh-Hant', 'zh-Hans', 'ja', 'es')
    app_schema: dict = {
        "@type": "SoftwareApplication",
        "name": 'KoreanGo Travel Korean',
        "softwareVersion": '1.0.0',
        "operatingSystem": "iOS 17.0+, iPadOS 17.0+",
        "applicationCategory": "EducationApplication",
        "url": ORIGIN,
        "image": f"{ORIGIN}/images/og.png",
        "inLanguage": list(site_langs),
        "isAccessibleForFree": True,
        "offers": [
            {"@type": "Offer", "name": "Free Forever", "price": "0", "priceCurrency": "USD"},
            {"@type": "Offer", "name": "KoreanGo Pro Lifetime", "price": "3.99", "priceCurrency": "USD"},
        ],
        "publisher": {"@id": "https://appengine.fun/#organization"},
    }
    if APP_STORE_URL:
        app_schema["downloadUrl"] = APP_STORE_URL
        app_schema["installUrl"] = APP_STORE_URL
    graph: list[dict] = [
        {
            "@type": "Organization",
            "@id": "https://appengine.fun/#organization",
            "name": "AE Interactive",
            "url": "https://appengine.fun/",
            "sameAs": ["https://www.youtube.com/@appengine-a", "https://languages.appengine.fun/"],
        },
        {
            "@type": "WebSite",
            "@id": f"{ORIGIN}/#website",
            "name": 'KoreanGo',
            "url": f"{ORIGIN}/",
            "inLanguage": list(site_langs),
            "publisher": {"@id": "https://appengine.fun/#organization"},
        },
        app_schema,
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "AE Interactive", "item": "https://appengine.fun/"},
                {"@type": "ListItem", "position": 2, "name": "AE Languages", "item": "https://languages.appengine.fun/"},
                {"@type": "ListItem", "position": 3, "name": 'KoreanGo', "item": f"{ORIGIN}/"},
            ] + (
                [{"@type": "ListItem", "position": 4, "name": title, "item": canon_url}]
                if canonical_path != "/"
                else []
            ),
        },
    ]
    if faq_items:
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": h, "acceptedAnswer": {"@type": "Answer", "text": p}}
                for h, p in faq_items
            ],
        })
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    smart_banner = f'<meta name="apple-itunes-app" content="app-id={APP_STORE_ID}">\n' if APP_STORE_ID else ""
    alternates = "".join(
        f'<link rel="alternate" hreflang="{code}" href="{ORIGIN}{canonical_path}' + ("" if code == "en" else f"?lang={code}") + '">\n'
        for code in site_langs
    )
    og_loc = OG_LOCALES.get(lang, "en_US")
    og_loc_alts = "".join(
        f'<meta property="og:locale:alternate" content="{OG_LOCALES[c]}">\n'
        for c in site_langs if c != lang
    )
    return f"""<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_mod.escape(title)}</title>
<meta name="description" content="{html_mod.escape(t['desc'])}">
<meta name="keywords" content="{html_mod.escape(t['keywords'])}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="author" content="AE Interactive">
<meta name="theme-color" content="#070913">
{smart_banner}<link rel="canonical" href="{canon_url}">
{alternates}<link rel="alternate" hreflang="x-default" href="{ORIGIN}{canonical_path}">
<link rel="icon" type="image/png" href="/images/icon.png">
<link rel="apple-touch-icon" href="/images/icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AE Interactive">
<meta property="og:locale" content="{og_loc}">
{og_loc_alts}<meta property="og:title" content="{html_mod.escape(title)}">
<meta property="og:description" content="{html_mod.escape(t['desc'])}">
<meta property="og:url" content="{canon_url}">
<meta property="og:image" content="{ORIGIN}/images/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html_mod.escape(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html_mod.escape(title)}">
<meta name="twitter:description" content="{html_mod.escape(t['desc'])}">
<meta name="twitter:image" content="{ORIGIN}/images/og.png">
<meta name="twitter:image:alt" content="{html_mod.escape(title)}">
<script type="application/ld+json">{schema}</script>
<style>{CSS}</style>
</head>"""


def build_home(lang: str, t: dict) -> str:
    q = f"?lang={lang}"
    audio_cards = []
    for idx, item in enumerate(AUDIO_ITEMS):
        play_lbl = html_mod.escape(t["btn_play"])
        playing_lbl = html_mod.escape(t["btn_playing"])
        audio_cards.append(f"""
        <article class="audio-card" id="card-{idx}">
          <div>
            <div class="audio-tag">{html_mod.escape(item['tag'][lang])}</div>
            <div class="audio-ko">{html_mod.escape(item['ko'])}</div>
            <div class="audio-roman">{item['roman']}</div>
            <div class="audio-ipa">{html_mod.escape(item['ipa'])}</div>
            <div class="audio-meaning">{html_mod.escape(item['meaning'][lang])}</div>
          </div>
          <button type="button" class="play-btn" onclick="togglePhrase('p{idx}','/audio/{item['file']}',this,document.getElementById('card-{idx}'),'{play_lbl}','{playing_lbl}')">▶ {play_lbl}</button>
        </article>""")

    shot_cards = []
    for i in range(1, 6):
        lbl = html_mod.escape(t["screens_labels"][i - 1])
        shot_cards.append(f"""
        <div class="shot-card">
          <img src="/images/{lang}_s0{i}.webp" alt="{lbl}" loading="lazy" width="640" height="1390">
          <div class="shot-cap">{lbl}</div>
        </div>""")
    ipad_lbl = html_mod.escape(t["screens_labels"][5])
    shot_cards.append(f"""
        <div class="shot-card wide">
          <img src="/images/{lang}_ipad.webp" alt="{ipad_lbl}" loading="lazy" width="760" height="1013">
          <div class="shot-cap">{ipad_lbl}</div>
        </div>""")

    bento_cards = []
    for icon, title, body in t["features"]:
        bento_cards.append(f"""
        <article class="bento-card">
          <div class="bento-icon" aria-hidden="true">{icon}</div>
          <h3>{html_mod.escape(title)}</h3>
          <p>{html_mod.escape(body)}</p>
        </article>""")

    free_lis = "".join(f'<li><span class="chk">✓</span><span>{html_mod.escape(x)}</span></li>' for x in t["free_tier_items"])
    pro_lis = "".join(f'<li><span class="chk">✓</span><span>{html_mod.escape(x)}</span></li>' for x in t["pro_tier_items"])

    if APP_STORE_URL:
        primary_store_btn = (
            f'<a class="btn btn-appstore" href="{APP_STORE_URL}" target="_blank" rel="noopener noreferrer">'
            f'{appstore_badge_svg()}'
            f'<span class="as-copy"><span class="as-sub">{html_mod.escape(t["cta_store_sub"])}</span>'
            f'<span class="as-main">{html_mod.escape(t["cta_store_main"])}</span></span></a>'
        )
        free_cta = f'<a class="btn btn-ghost" style="justify-content:center;" href="{APP_STORE_URL}" target="_blank" rel="noopener noreferrer">{html_mod.escape(t["appstore_btn_label"])}</a>'
        hero_actions = f'{primary_store_btn}<a class="btn btn-primary" href="#audio">{html_mod.escape(t["cta_audio"])}</a><a class="btn btn-ghost" href="#preview">{html_mod.escape(t["cta_screens"])}</a>'
    else:
        primary_store_btn = (
            f'<a class="btn btn-appstore" href="/support{q}">'
            f'{appstore_badge_svg()}'
            f'<span class="as-copy"><span class="as-sub">iPhone &amp; iPad</span>'
            f'<span class="as-main">{html_mod.escape(t["cta_coming_main"])}</span></span></a>'
        )
        free_cta = f'<a class="btn btn-ghost" style="justify-content:center;" href="#features">{html_mod.escape(t["appstore_btn_label"])}</a>'
        hero_actions = f'<a class="btn btn-primary" href="#audio">{html_mod.escape(t["cta_audio"])}</a><a class="btn btn-ghost" href="#preview">{html_mod.escape(t["cta_screens"])}</a><a class="btn btn-ghost" href="#pricing">{html_mod.escape(t["cta_plans"])}</a>'

    return f"""{head_html(lang, t, t['title'], '/')}
<body>
{nav_html(lang, '/', t)}
<main>
  <section class="hero">
    <div class="badge">{html_mod.escape(t['hero_badge'])}</div>
    <h1>{t['hero_title']}</h1>
    <p class="hero-sub">{html_mod.escape(t['hero_sub'])}</p>
    <div class="status-pill"> {html_mod.escape(t['status_pill'])}</div>
    <div class="hero-cta">
      {hero_actions}
    </div>
  </section>

  <section id="audio">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_audio_badge'])}</div>
      <h2>{html_mod.escape(t['sec_audio_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['sec_audio_sub'])}</p>
    </div>
    <div class="audio-grid">{''.join(audio_cards)}</div>
  </section>

  <section id="preview">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_screens_badge'])}</div>
      <h2>{html_mod.escape(t['sec_screens_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['sec_screens_sub'])}</p>
    </div>
    <div class="gallery-strip">{''.join(shot_cards)}</div>
  </section>

  <section id="features">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_features_badge'])}</div>
      <h2>{html_mod.escape(t['sec_features_title'])}</h2>
    </div>
    <div class="bento">{''.join(bento_cards)}</div>
  </section>

  <section id="pricing">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_pricing_badge'])}</div>
      <h2>{html_mod.escape(t['sec_pricing_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['sec_pricing_sub'])}</p>
    </div>
    <div class="pricing-grid">
      <article class="price-card">
        <div>
          <div class="price-head">
            <div>
              <div class="price-tag">{html_mod.escape(t['free_tier_tag'])}</div>
              <div class="price-title">{html_mod.escape(t['free_tier_title'])}</div>
            </div>
            <div class="price-num">{html_mod.escape(t['free_tier_price'])}</div>
          </div>
          <ul class="price-list" style="margin-top:16px;">{free_lis}</ul>
        </div>
        {free_cta}
      </article>
      <article class="price-card pro">
        <div>
          <div class="price-head">
            <div>
              <div class="price-tag">{html_mod.escape(t['pro_tier_badge'])}</div>
              <div class="price-title">{html_mod.escape(t['pro_tier_title'])}</div>
            </div>
            <div class="price-num">{html_mod.escape(t['pro_tier_price'])}</div>
          </div>
          <ul class="price-list" style="margin-top:16px;">{pro_lis}</ul>
        </div>
        {primary_store_btn}
      </article>
    </div>
  </section>

  <section class="cta-banner">
    <img src="/images/icon.webp" alt="KoreanGo" width="64" height="64">
    <h2>{html_mod.escape(t['bottom_cta_title'])}</h2>
    <p>{html_mod.escape(t['bottom_cta_sub'])}</p>
    {primary_store_btn}
  </section>
</main>
{footer_html(lang, t)}
<script>{SCRIPT_JS}</script>
</body>
</html>"""


def build_doc_page(lang: str, t: dict, route: str, heading: str, sub: str, items: list[tuple[str, str]]) -> str:
    blocks = "".join(
        f'<div class="doc-item"><h2>{html_mod.escape(h)}</h2><p>{html_mod.escape(p)}</p></div>'
        for h, p in items
    )
    faq = items if route == '/support' else None
    return f"""{head_html(lang, t, heading + ' | KoreanGo', route, faq_items=faq)}
<body>
{nav_html(lang, route, t)}
<main>
  <article class="doc-box">
    <h1>{html_mod.escape(heading)}</h1>
    <p style="color:var(--teal);font-weight:700;font-size:14px;margin-top:8px;">{html_mod.escape(sub)}</p>
    {blocks}
  </article>
</main>
{footer_html(lang, t)}
</body>
</html>"""


def cf_request(method: str, path: str, token: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4{path}", data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def deploy_worker(token: str, worker_js: str) -> None:
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{SCRIPT_NAME}"
    boundary = "----KoreanGoBoundary918273"
    body = [
        f"--{boundary}".encode(),
        b'Content-Disposition: form-data; name="metadata"',
        b"Content-Type: application/json",
        b"",
        json.dumps({"main_module": "index.js", "compatibility_date": "2024-03-03"}).encode(),
        f"--{boundary}".encode(),
        b'Content-Disposition: form-data; name="index.js"; filename="index.js"',
        b"Content-Type: application/javascript+module",
        b"",
        worker_js.encode("utf-8"),
        f"--{boundary}--".encode(),
        b"",
    ]
    req = urllib.request.Request(
        url,
        data=b"\r\n".join(body),
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        res = json.loads(resp.read())
        assert res.get("success"), f"Worker upload failed: {res}"
        print("WORKER_UPLOADED:", SCRIPT_NAME)


def ensure_dns_and_route(token: str) -> None:
    dns = cf_request("GET", f"/zones/{ZONE_ID}/dns_records?name={HOSTNAME}", token)
    existing = dns.get("result", [])
    if not existing:
        created = cf_request("POST", f"/zones/{ZONE_ID}/dns_records", token, {
            "type": "A",
            "name": HOSTNAME,
            "content": "192.0.2.1",
            "proxied": True,
            "ttl": 1,
        })
        assert created.get("success"), f"DNS create failed: {created}"
        print("DNS_CREATED:", HOSTNAME)
    else:
        print("DNS_EXISTS:", [(r["type"], r["name"], r["content"], r["proxied"]) for r in existing])

    routes = cf_request("GET", f"/zones/{ZONE_ID}/workers/routes", token).get("result", [])
    pattern = f"{HOSTNAME}/*"
    match = [r for r in routes if r.get("pattern") == pattern]
    if not match:
        rc = cf_request("POST", f"/zones/{ZONE_ID}/workers/routes", token, {
            "pattern": pattern,
            "script": SCRIPT_NAME,
        })
        assert rc.get("success"), f"Route create failed: {rc}"
        print("ROUTE_CREATED:", pattern, "->", SCRIPT_NAME)
    else:
        rid = match[0]["id"]
        if match[0].get("script") != SCRIPT_NAME:
            cf_request("PUT", f"/zones/{ZONE_ID}/workers/routes/{rid}", token, {
                "pattern": pattern,
                "script": SCRIPT_NAME,
            })
            print("ROUTE_UPDATED:", pattern, "->", SCRIPT_NAME)
        else:
            print("ROUTE_EXISTS:", pattern, "->", SCRIPT_NAME)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build-only", action="store_true", help="Build HTML & worker.js locally without uploading to Cloudflare")
    args = ap.parse_args()

    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    pages = {}
    privacy_pages = {}
    support_pages = {}
    for code, t in CONTENT.items():
        home_html = build_home(code, t)
        priv_html = build_doc_page(code, t, "/privacy", t["privacy_title"], t["privacy_updated"], t["privacy_sections"])
        supp_html = build_doc_page(code, t, "/support", t["support_title"], t["support_sub"], t["support_cards"])
        pages[code] = home_html
        privacy_pages[code] = priv_html
        support_pages[code] = supp_html
        suffix = "" if code == "en" else f"_{code}"
        (PUBLIC_DIR / f"index{suffix}.html").write_text(home_html, encoding="utf-8")
        (PUBLIC_DIR / f"privacy{suffix}.html").write_text(priv_html, encoding="utf-8")
        (PUBLIC_DIR / f"support{suffix}.html").write_text(supp_html, encoding="utf-8")

    images = {p.name: base64.b64encode(p.read_bytes()).decode("ascii") for p in sorted(IMG_DIR.glob("*"))}
    audio = {p.name: base64.b64encode(p.read_bytes()).decode("ascii") for p in sorted(AUD_DIR.glob("*.mp3"))}

    _site_langs = ('en', 'zh-Hant', 'zh-Hans', 'ja', 'es')
    def _sm_entry(path: str, code: str, prio: str) -> str:
        loc = f"{ORIGIN}{path}" if code == "en" else f"{ORIGIN}{path}?lang={code}"
        links = "\n".join(
            [f'    <xhtml:link rel="alternate" hreflang="{c}" href="{ORIGIN}{path}' + ("" if c == "en" else f"?lang={c}") + '"/>' for c in _site_langs]
            + [f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ORIGIN}{path}"/>']
        )
        return f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-11-26</lastmod>\n{links}\n    <priority>{prio}</priority>\n  </url>"

    sitemap_urls = "\n".join(
        [_sm_entry("/", c, "1.0" if c == "en" else "0.9") for c in _site_langs]
        + [_sm_entry("/privacy", "en", "0.7"), _sm_entry("/support", "en", "0.7")]
    )
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{sitemap_urls}\n</urlset>'
    robots_txt = f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n"

    worker_js = f"""const PAGES = {json.dumps(pages)};
const PRIVACY_PAGES = {json.dumps(privacy_pages)};
const SUPPORT_PAGES = {json.dumps(support_pages)};
const IMAGES = {json.dumps(images)};
const AUDIO = {json.dumps(audio)};
const SITEMAP = {json.dumps(sitemap_xml)};
const ROBOTS = {json.dumps(robots_txt)};

function b64ToBytes(b64) {{
  const s = atob(b64);
  const out = new Uint8Array(s.length);
  for (let i = 0; i < s.length; i++) out[i] = s.charCodeAt(i);
  return out;
}}

function resolveLang(request) {{
  const url = new URL(request.url);
  const q = url.searchParams.get("lang");
  if (q && PAGES[q]) return q;
  if (q === "zh-TW" || q === "tw" || q === "hk") return "zh-Hant";
  if (q === "zh-CN" || q === "cn" || q === "zh") return "zh-Hans";
  if (q === "jp" || q === "ja-JP") return "ja";
  if (q === "es-ES" || q === "es-MX") return "es";
  const accept = (request.headers.get("accept-language") || "").toLowerCase();
  if (accept.includes("zh-tw") || accept.includes("zh-hk") || accept.includes("zh-hant")) return "zh-Hant";
  if (accept.includes("zh")) return "zh-Hans";
  if (accept.includes("ja")) return "ja";
  if (accept.includes("es")) return "es";
  return "en";
}}

export default {{
  async fetch(request) {{
    const pathname = new URL(request.url).pathname;
    if (pathname === "/sitemap.xml") {{
      return new Response(SITEMAP, {{ headers: {{ "content-type": "application/xml;charset=UTF-8", "cache-control": "public, max-age=86400" }} }});
    }}
    if (pathname === "/robots.txt") {{
      return new Response(ROBOTS, {{ headers: {{ "content-type": "text/plain;charset=UTF-8", "cache-control": "public, max-age=86400" }} }});
    }}
    if (pathname.startsWith("/images/")) {{
      const name = pathname.slice("/images/".length);
      if (IMAGES[name]) {{
        const ct = name.endsWith(".png") ? "image/png" : "image/webp";
        return new Response(b64ToBytes(IMAGES[name]), {{ headers: {{ "content-type": ct, "cache-control": "public, max-age=31536000, immutable" }} }});
      }}
      return new Response("Not Found", {{ status: 404 }});
    }}
    if (pathname.startsWith("/audio/")) {{
      const name = pathname.slice("/audio/".length);
      if (AUDIO[name]) {{
        return new Response(b64ToBytes(AUDIO[name]), {{ headers: {{ "content-type": "audio/mpeg", "accept-ranges": "bytes", "cache-control": "public, max-age=31536000, immutable" }} }});
      }}
      return new Response("Not Found", {{ status: 404 }});
    }}
    const lang = resolveLang(request);
    const htmlHeaders = {{
      "content-type": "text/html;charset=UTF-8",
      "cache-control": "public, max-age=0, must-revalidate",
      "vary": "Accept-Language"
    }};
    if (pathname === "/privacy" || pathname === "/privacy.html") {{
      return new Response(PRIVACY_PAGES[lang] || PRIVACY_PAGES.en, {{ headers: htmlHeaders }});
    }}
    if (pathname === "/support" || pathname === "/support.html") {{
      return new Response(SUPPORT_PAGES[lang] || SUPPORT_PAGES.en, {{ headers: htmlHeaders }});
    }}
    return new Response(PAGES[lang] || PAGES.en, {{ headers: htmlHeaders }});
  }}
}};
"""
    (BASE_DIR / "worker.js").write_text(worker_js, encoding="utf-8")
    print(f"BUILT_WORKER: {len(worker_js) / 1024:.1f} KB ({len(images)} images, {len(audio)} audio)")

    if args.build_only:
        print("BUILD_ONLY_COMPLETE")
        return

    token = os.environ.get("CF_API_TOKEN", "").strip()
    if not token:
        token = Path("~/.cf_token").expanduser().read_text().strip()
    deploy_worker(token, worker_js)
    ensure_dns_and_route(token)
    print("DEPLOY_COMPLETE:", ORIGIN)


if __name__ == "__main__":
    main()
