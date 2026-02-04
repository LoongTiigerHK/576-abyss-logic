import streamlit as st
import plotly.graph_objects as go

import plotly.graph_objects as go
import numpy as np
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
# use_container_width=True 是适配手机的关键
st.plotly_chart(fig, use_container_width=True, theme="streamlit")
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

# 逻辑路径（立方体的棱）
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
    x_coords = [edge[0][0], edge[1][0]]
    y_coords = [edge[0][1], edge[1][1]]
    z_coords = [edge[0][2], edge[1][2]]
    fig.add_trace(go.Scatter3d(x=x_coords, y=y_coords, z=z_coords,
                               mode='lines', line=dict(color='cyan', width=2),
                               hoverinfo='none', showlegend=False))

# 2. 绘制顶点
x_v, y_v, z_v, labels = [], [], [], []
colors = []
for (x, y, z), (name, symbol) in vertices.items():
    x_v.append(x)
    y_v.append(y)
    z_v.append(z)
    labels.append(f"{symbol} {name}<br>({x},{y},{z})")
    # 颜色区分：乾坤两极
    if (x,y,z) == (1,1,1): colors.append('gold')
    elif (x,y,z) == (2,2,2): colors.append('magenta')
    else: colors.append('#00FFCC')

fig.add_trace(go.Scatter3d(x=x_v, y=y_v, z=z_v, mode='markers+text',
                           marker=dict(size=10, color=colors, line=dict(color='white', width=1)),
                           text=labels, textposition="top center",
                           hoverinfo='text', name="Trigrams"))

# 3. 绘制“否卦”红色虚线 (天地不交)
fig.add_trace(go.Scatter3d(x=[1, 2], y=[1, 2], z=[1, 2],
                           mode='lines', line=dict(color='red', width=4, dash='dash'),
                           name="Pi (Stagnation) Path"))

# 4. 增加“恒”字共鸣中心点
fig.add_trace(go.Scatter3d(x=[1.5], y=[1.5], z=[1.5],
                           mode='markers', marker=dict(size=15, color='white', symbol='diamond', line=dict(width=1, color='white')),
                           name="Logical Center",
                           hovertext="Logical Center"))

# --- 视觉修饰 ---
fig.update_layout(
    scene = dict(
        xaxis = dict(title='初爻 (Bottom Line)', backgroundcolor="#050505", gridcolor="gray", zerolinecolor="gray"),
        yaxis = dict(title='中爻 (Middle Line)', backgroundcolor="#050505", gridcolor="gray", zerolinecolor="gray"),
        zaxis = dict(title='上爻 (Top Line)', backgroundcolor="#050505", gridcolor="gray", zerolinecolor="gray"),
        aspectmode='cube' # 保持比例
    ),
    title={'text': '八卦布尔逻辑 Boolean Space 3D Visualization (Plotly)', 'font': {'color': 'gold', 'size': 20}},
    paper_bgcolor='#050505',
    plot_bgcolor='#050505',
    font=dict(color='white'),
    showlegend=True,
    height=800
)


st.plotly_chart(fig, use_container_width=True)


