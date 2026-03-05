#!/data/data/com.termux/files/usr/bin/bash
# Imperial Gemini Command Center
cd ~/imperial_network

case "$1" in
    quota)
        python3 gemini/quota_tracker.py
        ;;
    test)
        python3 gemini/test_gemini.py
        ;;
    strategy)
        python3 gemini/malamulele_strategy.py
        ;;
    status)
        echo "🏛️ IMPERIAL GEMINI STATUS"
        echo "========================"
        echo "API Key: ${GEMINI_API_KEY:0:15}..."
        python3 gemini/quota_tracker.py | head -5
        ;;
    *)
        echo "Usage: imperial_gemini.sh {quota|test|strategy|status}"
        ;;
esac
