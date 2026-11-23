# KoreanGo — Travel Korean & Live Voice Translation Website

Official marketing, native audio preview, privacy policy, and support website for **KoreanGo Travel Korean** ([AE Interactive](https://appengine.fun)).

- **Live Website:** https://koreango.appengine.fun
- **Privacy Policy:** https://koreango.appengine.fun/privacy
- **Support & FAQ:** https://koreango.appengine.fun/support
- **App Bundle ID:** `com.chiangkevin.koreango`

## Features
- **4 Languages Supported:** English (`/`), Traditional Chinese (`/?lang=zh-Hant`), Simplified Chinese (`/?lang=zh-Hans`), and Japanese (`/?lang=ja`).
- **Interactive Native Korean Phrase Previews:** In-app studio MP3 playback highlighting Seoul tense consonants (`ㄸ`), liaison (`갈아타요`), time counters (`몇 시`), and soft `ㅎ` (`천천히`).
- **Product & Pricing Clarity:** App screenshots across iPhone 6.9" and iPad 13", 6 integrated modules (`40 Hangul Jamo + Stroke Canvas`, `24 Minimal Pairs`, `15 Lessons + 18 Grammar Drills`, `100 Seoul Video Dialogues`, `12-Scene Guided Voice Practice`, `Live 2-Way ko-KR Interpreter`), and `Free Forever` vs. `$3.99 KoreanGo Pro Lifetime` comparison.
- **Localized `/privacy` & `/support`:** Zero-data-collection privacy commitment (`NSPrivacyTracking = false`) and offline translation pack instructions.
- **Cloudflare Worker Edge Bundle:** Single-file edge deployment serving localized HTML, WebP screenshots, OG card, and studio MP3 audio clips cleanly.

## Build & Deploy
```bash
python3 prepare_assets.py
python3 build_and_deploy.py
```
