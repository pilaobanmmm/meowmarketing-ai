"""MeowMarketing AI: beginner-friendly marketing content planner.

Stage 1: content calendar with no API key (rule-based, NOT AI generated).
Stage 2: optional real AI-powered content suggestions with OpenAI API.
"""

import os
from datetime import date, timedelta

import pandas as pd
import streamlit as st


st.set_page_config(page_title="MeowMarketing AI", page_icon="🐱", layout="wide")
st.title("🐱 MeowMarketing AI")
st.caption("营销内容排期与 AI 创意助手｜求职作品集入门版")

with st.sidebar:
    st.header("📋 营销需求")
    brand = st.text_input("品牌名称", value="喵喵美妆")
    product = st.text_input("推广产品", value="水光唇釉")
    audience = st.text_input("目标用户", value="18–25 岁、喜欢日常妆容的学生和年轻职场人")
    platform = st.selectbox("投放平台", ["小红书", "抖音", "微信公众号"])
    goal = st.selectbox("营销目标", ["品牌认知", "互动种草", "引流转化"])
    tone = st.selectbox("内容风格", ["真实亲切", "专业科普", "活泼有趣"])
    days = st.select_slider("排期天数", options=[7, 14], value=7)
    start_date = st.date_input("开始日期", value=date.today())
    create_plan = st.button("生成内容排期", use_container_width=True, type="primary")

# These are human-authored demo templates. They are NOT AI output.
ANGLES = [
    ("用户痛点", "你是不是也遇到这些{product}使用困扰？", "征集用户真实使用痛点，整理常见问题"),
    ("产品亮点", "认识一下{brand}的{product}", "介绍可核实的产品特点，避免夸张承诺"),
    ("使用教程", "新手也能看懂的{product}使用指南", "用简明步骤讲解使用方法"),
    ("适用场景", "什么场景适合使用{product}？", "围绕目标用户的典型生活情境给出创意"),
    ("互动话题", "关于{product}，你最想了解什么？", "用问题引导评论、收集后续选题"),
    ("用户反馈", "大家关心的{product}问题整理", "总结授权使用的真实反馈或明确标注示例"),
    ("回顾总结", "这一周关于{product}的七个发现", "回顾内容重点，并记录后续优化方向"),
]


def build_plan(brand_name, product_name, platform_name, audience_name, goal_name, tone_name, days_count, beginning):
    rows = []
    for index in range(days_count):
        topic, title, suggestion = ANGLES[index % len(ANGLES)]
        rows.append(
            {
                "日期": (beginning + timedelta(days=index)).isoformat(),
                "平台": platform_name,
                "内容方向": topic,
                "建议标题": title.format(brand=brand_name, product=product_name),
                "内容要点": suggestion,
                "目标人群": audience_name,
                "营销目标": goal_name,
                "文案风格": tone_name,
                "状态": "待制作",
            }
        )
    return pd.DataFrame(rows)


if create_plan:
    if not brand.strip() or not product.strip() or not audience.strip():
        st.error("请先填写品牌、产品和目标用户。")
    else:
        st.session_state["calendar"] = build_plan(
            brand.strip(), product.strip(), platform, audience.strip(), goal, tone, days, start_date
        )
        st.session_state["brief"] = {
            "品牌": brand.strip(), "产品": product.strip(), "目标人群": audience.strip(),
            "平台": platform, "营销目标": goal, "风格": tone,
        }
        st.session_state.pop("ai_content", None)

if "calendar" not in st.session_state:
    st.info("👈 先在左侧填写营销需求，再点击「生成内容排期」。")
    st.write("第一阶段可以不配置 API Key：先让排期和 CSV 导出顺利工作。")
else:
    calendar = st.session_state["calendar"]
    st.subheader("📅 内容排期")
    col1, col2, col3 = st.columns(3)
    col1.metric("计划内容", len(calendar))
    col2.metric("覆盖平台", calendar["平台"].nunique())
    col3.metric("不同选题方向", calendar["内容方向"].nunique())
    st.dataframe(calendar, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ 导出 CSV（Excel 可打开）",
        data=calendar.to_csv(index=False).encode("utf-8-sig"),
        file_name="meowmarketing_content_calendar.csv", mime="text/csv"
    )
    st.caption("目前的排期来自预设模板，不是 AI 生成，也不代表真实投放效果。")

    st.divider()
    st.subheader("✨ 第二阶段：AI 内容创意")
    st.write("AI 可以根据营销 Brief 与排期，给出具体的标题、正文草稿和话题标签。")
    st.caption("需要单独配置 OpenAI API Key；ChatGPT 订阅不等于 API 额度，API 可能产生费用。")
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        st.warning("尚未配置 OPENAI_API_KEY。排期与导出仍可正常使用。配置方法见 README_CN.md。")
    if st.button("生成 AI 内容创意", disabled=not bool(api_key)):
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            brief = st.session_state["brief"]
            details = calendar[["日期", "内容方向", "建议标题"]].to_string(index=False)
            instruction = (
                "你是一位谨慎、了解中文社交媒体营销的内容策划。"
                "请根据下面的营销 Brief 和排期，按日期逐条输出中文营销创意。"
                "每条包含：内容标题、80字以内的正文初稿、2-4个话题标签、一个互动问题。"
                "不要编造销量、用户评价、实际转化数据或产品功效；"
                "不要假装已进行市场调研或发布内容。明确任何需要品牌核实的卖点。\n\n"
                f"营销 Brief：{brief}\n\n内容排期：\n{details}"
            )
            with st.spinner("正在生成内容创意…"):
                response = client.responses.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    input=instruction,
                )
            st.session_state["ai_content"] = response.output_text
        except Exception as exc:
            st.error(f"AI 请求失败，请检查 API 设置与账户额度。错误类型：{type(exc).__name__}")
    if "ai_content" in st.session_state:
        st.markdown(st.session_state["ai_content"])
        st.download_button(
            "⬇️ 下载 AI 创意草稿",
            data=st.session_state["ai_content"].encode("utf-8"),
            file_name="meowmarketing_ai_ideas.txt", mime="text/plain",
        )

st.divider()
st.caption("作品集练习项目｜AI 辅助开发｜请标注数据来源、人工审核生成内容")
