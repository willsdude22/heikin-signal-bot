📦 Simple 15s Heikin Ashi Signal Bot (Render)

✅ Uses:
- SMA 5 & SMA 10 crossover
- RSI 14 filter (BUY if < 70, SELL if > 30)
- Volume confirmation (must be above/below average)
- Entry time in EST
- Currency and OTC pairs only

📩 TradingView JSON:
{
  "symbol": "{{ticker}}",
  "sma5": {{plot_0}},
  "sma10": {{plot_1}},
  "rsi": {{plot_2}},
  "volume": {{volume}},
  "avg_volume": {{plot_3}}
}

🚀 Deployment:
1. Upload this ZIP to GitHub
2. Connect it to https://render.com
3. Use:
   - Build: pip install -r requirements.txt
   - Start: python main.py
   - Port: 10000