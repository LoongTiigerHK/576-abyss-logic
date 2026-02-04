import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 1. 页面基本配置（必须在最前面，不能重复）
st.set_page_config(
    page_title="576-Abyss-Logic", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 注入 CSS 抹平手机端边距
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌌 576-Abyss-Logic 观测站")

# --- 数据定义 ---
# 坐标 (初爻, 中爻, 上爻) | 1=阳, 2=阴
vertices = {
    (1, 1, 1): ("Qian (乾)", "☰"),
    (2, 1, 1): ("Xun (巽)", "☴"),
    (1, 2, 1): ("Li (离)", "☲"),
    (2, 2, 1): ("Gen (艮)", "☶"),
    (1, 1, 2): ("Dui (兑)", "☱"),
    (2, 1, 2): ("Kan (坎)", "☵"),
    (1, 2, 2): ("Zhen (震)", "☳"),
    (2, 2, 2): ("Kun (坤)", "☷")
}

edges = [
    ((1,1,1), (2,1,1)), ((1,1,1), (1,2,1)), ((1,1,1), (1,1,2)),
    ((2,2,2), (1,2,2)), ((2,2,2), (2,1,2)), ((2,2,2), (2,2,1)),
    ((2,1,1), (2,2,1)), ((2,1,1), (2,1,2)),
    ((1,2,1), (2,2,1)), ((1,2,1), (1,2,2)),
    ((1,1,2), (2,1,2)), ((1,1,2), (1,2,2))
]

fig = go.Figure()

# 1. 绘制逻辑连线
for edge in edges:
    fig.add_trace(go.Scatter3d(
        x=[edge[0][0], edge[1][0]],
        y=[edge[0][1], edge[1][1]],
        z=[edge[0][2], edge[1][2]],
        mode='lines', 
        line=dict(color='cyan', width=2),
        hoverinfo='none', 
        showlegend=False
    ))

# 2. 绘制顶点
x_v, y_v, z_v, labels, colors = [], [], [], [], []
for (x, y, z), (name, symbol) in vertices.items():
    x_v.append(x)
    y_v.append(y)
    z_v.append(z)
    labels.append(f"{symbol} {name}")
    if (x,y,z) == (1,1,1): colors.append('gold')
    elif (x,y,z) == (2,2,2): colors.append('magenta')
    else: colors.append('#00FFCC')

fig.add_trace(go.Scatter3d(
    x=x_v, y=y_v, z=z_v, 
    mode='markers+text',
    marker=dict(size=8, color=colors, line=dict(color='white', width=1)),
    text=labels, 
    textposition="top center",
    name="八卦位点"
))

# 3. 增加“恒”中心点
fig.add_trace(go.Scatter3d(
    x=[1.5], y=[1.5], z=[1.5],
    mode='markers+text',
    marker=dict(size=12, color='red', symbol='diamond'),
    text=["恒 (Center)"],
    textposition="bottom center",
    name="中心共鸣"
))

# --- 视觉修饰与手机适配 ---
fig.update_layout(
    scene = dict(
        xaxis = dict(title='初', range=[0.5, 2.5], backgroundcolor="#050505", gridcolor="gray"),
        yaxis = dict(title='中', range=[0.5, 2.5], backgroundcolor="#050505", gridcolor="gray"),
        zaxis = dict(title='上', range=[0.5, 2.5], backgroundcolor="#050505", gridcolor="gray"),
        aspectmode='cube'
    ),
    paper_bgcolor='#050505',
    plot_bgcolor='#050505',
    font=dict(color='white'),
    margin=dict(l=0, r=0, b=0, t=0), # 关键：撑满手机宽度
    height=700,                      # 关键：手机端高度
    showlegend=False
)

# 4. 最终显示
st.plotly_chart(fig, use_container_width=True, theme=None, key="abyss_logic_v2")
