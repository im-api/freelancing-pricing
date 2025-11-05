# ============================================================
# 💼 MehT AI Pricing Engine v14 — English Inputs + Persian Output + Internal Net Table
# ============================================================

import tempfile, webbrowser
from pathlib import Path


def smart_price(rate_per_day, base_days, complexity=1.0, urgency=1.0,
                client_value=1.0, confidence=1.0, platform_fee=0.0):
    """Core pricing logic including platform commission."""
    base_price = rate_per_day * base_days
    effort_factor = complexity * urgency
    value_factor = (client_value + confidence) / 2
    fair_price = base_price * effort_factor * value_factor

    # Time–price tiers
    slow_1 = (base_days * 1.25, fair_price * 0.9 * confidence)
    slow_2 = (base_days * 1.5, fair_price * 0.8 * confidence)
    slow_3 = (base_days * 2.0, fair_price * 0.7 * confidence)
    fast_1 = (base_days * 0.85, fair_price * (1.15 + (urgency - 1) * 0.2))
    fast_2 = (base_days * 0.7, fair_price * (1.35 + (urgency - 1) * 0.3))
    fast_3 = (base_days * 0.5, fair_price * (1.6 + (urgency - 1) * 0.5))

    tiers = {
        "پیشنهاد اقتصادی (زمان تحویل بیشتر)": slow_1,
        "پیشنهاد استاندارد توسعه‌یافته": slow_2,
        "پیشنهاد بلندمدت (تحویل بسیار منعطف)": slow_3,
        "پیشنهاد پایه (زمان و هزینه متعادل)": (base_days, fair_price),
        "پیشنهاد ویژه (تحویل سریع‌تر)": fast_1,
        "پیشنهاد پریمیوم (اولویت بالا)": fast_2,
        "پیشنهاد اجرایی (فوری و اختصاصی)": fast_3,
    }

    # Calculate both: client price (with commission) and net income
    result = {}
    for label, (days, price) in tiers.items():
        client_price = price / (1 - platform_fee / 100) if platform_fee > 0 else price
        net_income = price  # before markup
        result[label] = (days, client_price, net_income)

    avg_price = sum(v[1] for v in result.values()) / len(result)
    price_range = (min(v[1] for v in result.values()), max(v[1] for v in result.values()))
    return result, avg_price, price_range


def show_in_browser(prices, avg_price, price_range, inputs):
    """Display professional client-facing and internal tables."""
    rate, days, complexity, urgency, client_value, confidence, platform_fee = inputs

    # HTML output
    html_content = f"""
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>پیشنهاد قیمت پروژه</title>
        <style>
            body {{
                font-family: 'Vazirmatn','IRANSans','Tahoma',sans-serif;
                background:#f9fafb;color:#222;padding:2rem;direction:rtl;
            }}
            table {{
                border-collapse:collapse;width:100%;max-width:780px;margin:auto;
                background:white;border-radius:12px;
                box-shadow:0 0 12px rgba(0,0,0,0.1);
            }}
            th,td {{
                border-bottom:1px solid #ddd;text-align:right;padding:12px 16px;
            }}
            th {{
                background:#0c3f4b;color:#fff;font-size:1.05rem;
            }}
            tr:hover td {{background:#f7f7f7;}}
            caption {{
                caption-side:top;font-size:1.35rem;margin-bottom:15px;
                font-weight:bold;color:#0c3f4b;
            }}
            .summary {{
                margin-top:1.7rem;text-align:center;font-size:1.1rem;direction:rtl;
            }}
            .inputs {{
                margin-top:2rem;font-size:0.9rem;color:#555;
                direction:rtl;text-align:right;max-width:780px;margin:auto;
                border-top:1px dashed #bbb;padding-top:1rem;
            }}
            .inputs h3 {{ color:#0c3f4b; }}
            .footer {{
                text-align:center;margin-top:2rem;font-size:0.95rem;
                color:#555;border-top:1px solid #ccc;padding-top:1rem;
            }}
            .internal {{
                margin-top:1.5rem;
                font-size:0.9rem;
                border:1px solid #ccc;
                background:#fff;
                border-radius:8px;
                padding:10px 15px;
                max-width:780px;
                margin:auto;
            }}
            .internal caption {{
                font-size:1.05rem;
                color:#0c3f4b;
                margin-bottom:10px;
            }}
        </style>
    </head>
    <body>
        <!-- ===== CLIENT TABLE ===== -->
        <table>
            <caption>پیشنهاد قیمت پروژه </caption>
            <tr>
                <th>سطح پیشنهاد</th>
                <th>مدت زمان (روز)</th>
                <th>مبلغ نهایی (تومان)</th>
            </tr>
            {''.join(f'<tr><td>{label}</td><td>{value[0]:.1f} روز</td><td>{value[1]:,.0f} تومان</td></tr>' for label,value in prices.items())}
        </table>

        <div class="summary">
            <p>میانگین قیمت پیشنهادی: <b>{avg_price:,.0f} تومان</b></p>
            <p>بازهٔ کلی قیمت: از {price_range[0]:,.0f} تا {price_range[1]:,.0f} تومان</p>
            <p>✅ مبالغ فوق شامل {platform_fee:.0f}% کمیسیون پلتفرم هستند و برای ارائه به شما طراحی شده‌اند.</p>
        </div>

        <!-- ===== INTERNAL SECTION ===== -->
        <div class="inputs">
            <h3>⚙️ پارامترهای محاسبه:</h3>
            <p><b>نرخ پایه روزانه:</b> {rate:,.0f} تومان</p>
            <p><b>مدت زمان پایه پروژه:</b> {days} روز</p>
            <p><b>ضریب سختی کار:</b> {complexity}</p>
            <p><b>ضریب فوریت:</b> {urgency}</p>
            <p><b>ارزش مشتری:</b> {client_value}</p>
            <p><b>انگیزه یا تمایل شما:</b> {confidence}</p>
            <p><b>درصد کمیسیون پلتفرم:</b> {platform_fee}%</p>
        </div>

        <div class="internal">
            <caption>📊 جدول داخلی: درآمد خالص شما پس از کسر کمیسیون</caption>
            <table>
                <tr><th>سطح پیشنهاد</th><th>مدت زمان (روز)</th><th>درآمد خالص (تومان)</th></tr>
                {''.join(f'<tr><td>{label}</td><td>{value[0]:.1f} روز</td><td>{value[2]:,.0f} تومان</td></tr>' for label,value in prices.items())}
            </table>
        </div>

        <div class="footer">
            <p>تهیه‌شده با موتور قیمت‌گذاری هوشمند مهت</p>
            <p style="font-size:0.85rem;color:#777;">MehT AI Pricing Engine — Confidential Proposal</p>
        </div>
    </body>
    </html>
    """

    with tempfile.NamedTemporaryFile('w', delete=False, suffix=".html", encoding="utf-8") as f:
        f.write(html_content)
        temp_path = Path(f.name)
    webbrowser.open(temp_path.as_uri())


# ============================================================
# 🧮 Interactive English Inputs
# ============================================================
if __name__ == "__main__":
    print("=== 💼 MehT AI Pricing Engine v14 (English Inputs + Persian Output + Internal Net Table) ===")

    rate = float(input("💵 Base daily rate (IRT per day): "))
    days = int(input("🕒 Base project duration (days): "))
    complexity = float(input("⚙️ Project complexity (1 = normal, >1 = harder): "))
    urgency = float(input("⏱️ Urgency level (1 = normal, >1 = rush): "))
    client_value = float(input("🤝 Client value (1 = normal, >1 = VIP): "))
    confidence = float(input("💡 Your motivation/interest (1 = neutral, <1 = low): "))
    platform_fee = float(input("🌐 Platform commission percentage (e.g., 15): "))

    prices, avg_price, rng = smart_price(rate, days, complexity, urgency,
                                         client_value, confidence, platform_fee)
    show_in_browser(prices, avg_price, rng,
                    (rate, days, complexity, urgency, client_value, confidence, platform_fee))
