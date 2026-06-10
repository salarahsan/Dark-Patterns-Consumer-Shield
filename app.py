import sys
import types
import re

# 🚨 DYNAMIC FIX: Python 3.13 Compatibility Patches
if 'audioop' not in sys.modules:
    dummy_audioop = types.ModuleType('audioop')
    dummy_audioop.error = Exception
    sys.modules['audioop'] = dummy_audioop

import gradio as gr

def scan_dark_patterns(raw_html_or_text):
    if not raw_html_or_text.strip():
        return "<div style='color: #ef4444; font-weight: bold; padding: 10px;'>⚠️ Error: Please paste website HTML or text content to audit!</div>"
        
    text_to_scan = raw_html_or_text.strip()
    
    # 🔍 Technical Heuristics Matrix
    patterns = {
        "False Urgency & Fake Timers": [
            r"(?i)ends in \d+m", r"(?i)hurry up", r"(?i)limited time offer", 
            r"(?i)only \d+ left", r"(?i)demand is high", r"(?i)selling fast",
            r"stock running low", r"buying right now"
        ],
        "Social Proof Manipulation": [
            r"(?i)verified buyer", r"(?i)everyone else bought", r"(?i)someone from .* just purchased",
            r"(?i)5-star rated by thousand", r"trusted by millions"
        ],
        "Hidden Charges & Sneaking": [
            r"(?i)hidden fee", r"(?i)service charge added", r"(?i)protection plan auto-renew",
            r"(?i)convenience fee", r"handling charges apply at checkout"
        ],
        "Forced Continuity": [
            r"(?i)subscription auto-renews", r"(?i)no thanks, i hate saving money", 
            r"(?i)keep insurance active", r"cancel anytime\* condition"
        ]
    }
    
    detected_rows = ""
    total_violations = 0
    
    # Analyze string patterns natively and generate clean HTML rows
    for category, regex_list in patterns.items():
        matched_triggers = []
        for regex in regex_list:
            matches = re.findall(regex, text_to_scan)
            if matches:
                matched_triggers.extend([f"\"{m}\"" for m in matches])
                total_violations += len(matches)
                
        if matched_triggers:
            icon = "🚨" if "Charges" in category or "Urgency" in category else "⚠️"
            unique_triggers = list(set(matched_triggers)) # Deduplicate for clean view
            detected_rows += f"""
            <tr style='border-bottom: 1px solid #e2e8f0;'>
                <td style='padding: 12px; font-weight: 600; color: #1e293b;'>{icon} {category}</td>
                <td style='padding: 12px;'>
                    <span style='background-color: #fee2e2; color: #991b1b; padding: 4px 8px; border-radius: 6px; font-size: 13px; font-family: monospace; font-weight: 600;'>
                        {", ".join(unique_triggers)}
                    </span>
                </td>
            </tr>
            """
            
    # Risk Scoring Formula
    risk_score = min(100, total_violations * 25)
    
    if risk_score >= 75:
        verdict = "🔴 HIGH RISK (Highly Manipulative Tactics)"
        verdict_color = "#ef4444"
        bg_verdict = "#fef2f2"
    elif risk_score >= 40:
        verdict = "🟡 MEDIUM RISK (Deceptive Tricks Identified)"
        verdict_color = "#d97706"
        bg_verdict = "#fffbeb"
    else:
        verdict = "🟢 CLEAN / LOW RISK (Fair Consumer Practice)"
        verdict_color = "#16a34a"
        bg_verdict = "#f0fdf4"
        
    # Full Screen Render Pipeline Override (Eliminating code block leakage)
    if total_violations == 0:
        final_layout = """
        <div style='font-family: system-ui, sans-serif; padding: 5px;'>
            <div style='background-color: #f0fdf4; border-left: 5px solid #16a34a; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
                <h3 style='margin: 0; color: #16a34a; font-size: 18px;'>🛡️ Compliance Status: SECURE</h3>
                <p style='margin: 5px 0 0 0; color: #166534; font-size: 14px;'>No consumer manipulation or hidden traps detected.</p>
            </div>
            <div style='font-size: 16px; color: #0f172a;'><b>Consumer Threat Index:</b> <span style='color: #16a34a; font-weight: bold;'>0% Risk</span></div>
        </div>
        """
    else:
        final_layout = f"""
        <div style='font-family: system-ui, sans-serif; padding: 5px;'>
            
            <div style='background-color: {bg_verdict}; border-left: 5px solid {verdict_color}; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
                <h3 style='margin: 0; color: {verdict_color}; font-size: 18px;'>{verdict}</h3>
                <p style='margin: 5px 0 0 0; color: #475569; font-size: 14px;'>Forensic data metrics verified inside local edge matrix footprint.</p>
            </div>
            
            <div style='margin-bottom: 20px; font-size: 16px; color: #0f172a;'>
                <b>Consumer Threat Index:</b> 
                <span style='background-color: {verdict_color}; color: #ffffff; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 14px;'>
                    {risk_score}% Threat Level
                </span>
            </div>
            
            <h4 style='color: #0f172a; margin: 0 0 10px 0; font-size: 15px;'>🔍 Deceptive Breakdown (فریب کاری کی تفصیل):</h4>
            <table style='width: 100%; border-collapse: collapse; text-align: left; margin-bottom: 15px;'>
                <thead>
                    <tr style='background-color: #f8fafc; border-bottom: 2px solid #cbd5e1;'>
                        <th style='padding: 10px; color: #475569; font-size: 13px;'>Category</th>
                        <th style='padding: 10px; color: #475569; font-size: 13px;'>Detected Trigger Tokens</th>
                    </tr>
                </thead>
                <tbody>
                    {detected_rows}
                </tbody>
            </table>
            
            <p style='margin-top: 15px; font-size: 13px; color: #2563eb; font-style: italic; font-weight: 500; line-height: 1.4;'>
                💡 Shield Advice: Do not make panic purchases based on artificial countdown clocks or pre-checked hidden checkboxes.
            </p>
        </div>
        """
    return final_layout

# Premium Cyber-Shield Workspace Stylesheet Injection
custom_css = """
body, .gradio-container { background-color: #f8fafc !important; color: #0f172a !important; font-family: 'Segoe UI', system-ui, sans-serif; }
.shield-btn { background-color: #2563eb !important; color: #ffffff !important; font-weight: bold !important; border-radius: 8px !important; font-size: 16px !important; border: none !important; margin-top: 10px; height: 45px; }
.shield-btn:hover { background-color: #1d4ed8 !important; box-shadow: 0 4px 12px rgba(37,99,235,0.2); }
.panel-layout { border: 1px solid #e2e8f0 !important; border-radius: 12px; padding: 20px; background: #ffffff !important; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
textarea { background-color: #ffffff !important; color: #0f172a !important; border: 1px solid #cbd5e1 !important; font-size: 14px !important; }
label { color: #334155 !important; font-weight: 600 !important; }
"""

with gr.Blocks(title="Consumer Shield v1.0", css=custom_css, theme=gr.themes.Default(primary_hue="blue", secondary_hue="slate")) as demo:
    gr.HTML(
        """
        <div style="text-align: center; margin-bottom: 25px; padding: 20px; background: #2563eb; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <h1 style='margin: 0; font-size: 28px; color: #ffffff; letter-spacing: 0.5px; font-weight: 700;'>🛡️ DARK-PATTERNS CONSUMER SHIELD</h1>
            <p style='margin: 6px 0 0 0; color: #dbeafe; font-size: 14px; font-weight: 500;'>Serverless E-Commerce Protection & Pattern Audit Matrix // Zero-Latency Scanner</p>
        </div>
        """
    )
    
    with gr.Row():
        with gr.Column(scale=5, elem_classes="panel-layout"):
            gr.Markdown("### 🌐 Web Scraping & Ingestion Node")
            source_input = gr.Textbox(
                label="Paste Store Copy, Product Descriptions, or Web Raw HTML", 
                placeholder="Paste content here...",
                lines=12
            )
            scan_btn = gr.Button("🛡️ Launch Real-Time Forensic Audit", elem_classes="shield-btn")
            
        with gr.Column(scale=4, elem_classes="panel-layout"):
            gr.Markdown("### 📊 Shield Compliance Output Dashboard")
            
            # 🔥 FIXED: Changed component type to dynamic gr.HTML to properly execute layout layers
            audit_output = gr.HTML(
                "<div style='color: #64748b; font-style: italic; padding: 10px;'>Security Engine active. Waiting for raw e-commerce matrix data streams...</div>"
            )

    scan_btn.click(
        fn=scan_dark_patterns, 
        inputs=[source_input], 
        outputs=[audit_output]
    )

demo.launch()
