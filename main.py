import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import random
from pathlib import Path

st.set_page_config(page_title="Data Visualization Decision Study", layout="centered")

DATA = [
    {"id": 1, "task": "exact", "question": "What was the sales value in March?", "answer": "120",
     "months": ["Jan","Feb","Mar","Apr","May","Jun"], "values": [100,135,120,150,145,160]},
    {"id": 2, "task": "exact", "question": "What was the sales value in May?", "answer": "145",
     "months": ["Jan","Feb","Mar","Apr","May","Jun"], "values": [100,135,120,150,145,160]},
    {"id": 3, "task": "compare", "question": "Which month had the highest sales?", "answer": "Jun",
     "months": ["Jan","Feb","Mar","Apr","May","Jun"], "values": [100,135,120,150,145,160]},
    {"id": 4, "task": "compare", "question": "Which month had the lowest sales?", "answer": "Jan",
     "months": ["Jan","Feb","Mar","Apr","May","Jun"], "values": [100,135,120,150,145,160]},
    {"id": 5, "task": "trend", "question": "Between which consecutive months was the largest increase?", "answer": "Mar-Apr",
     "months": ["Jan","Feb","Mar","Apr","May","Jun"], "values": [100,135,120,150,145,160]},
    {"id": 6, "task": "trend", "question": "Did sales generally increase from January to June?", "answer": "Yes",
     "months": ["Jan","Feb","Mar","Apr","May","Jun"], "values": [100,135,120,150,145,160]},

    {"id": 7, "task": "exact", "question": "What was attendance in April?", "answer": "82",
     "months": ["Jan","Feb","Mar","Apr","May","Jun"], "values": [76,84,79,82,88,91]},
    {"id": 8, "task": "exact", "question": "What was attendance in February?", "answer": "84",
     "months": ["Jan","Feb","Mar","Apr","May","Jun"], "values": [76,84,79,82,88,91]},
    {"id": 9, "task": "compare", "question": "Which month had the highest attendance?", "answer": "Jun",
     "months": ["Jan","Feb","Mar","Apr","May","Jun"], "values": [76,84,79,82,88,91]},
    {"id": 10, "task": "compare", "question": "Which month had the lowest attendance?", "answer": "Jan",
     "months": ["Jan","Feb","Mar","Apr","May","Jun"], "values": [76,84,79,82,88,91]},
    {"id": 11, "task": "trend", "question": "Between which consecutive months was the largest increase?", "answer": "May-Jun",
     "months": ["Jan","Feb","Mar","Apr","May","Jun"], "values": [76,84,79,82,88,91]},
    {"id": 12, "task": "trend", "question": "Did attendance generally increase from January to June?", "answer": "Yes",
     "months": ["Jan","Feb","Mar","Apr","May","Jun"], "values": [76,84,79,82,88,91]},
]

OPTIONS = {
    "exact": ["120","145","150","160","82","84","88","91"],
    "compare": ["Jan","Mar","Apr","May","Jun","Feb"],
    "trend": ["Yes","No","Jan-Feb","Feb-Mar","Mar-Apr","Apr-May","May-Jun"]
}

def make_table(item):
    return pd.DataFrame({"Month": item["months"], "Value": item["values"]})

def draw_chart(item, chart_type):
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    if chart_type == "bar":
        ax.bar(item["months"], item["values"])
        ax.set_title("Data Display")
    else:
        ax.plot(item["months"], item["values"], marker="o")
        ax.set_title("Data Display")
    ax.set_xlabel("Month")
    ax.set_ylabel("Value")
    fig.tight_layout()
    return fig

def reset_study():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.title("Data Visualization and Decision-Making Study")

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.write("This prototype compares tables, bar charts, and line graphs using task accuracy, response time, and confidence.")
    participant = st.text_input("Participant ID (use an anonymous code)")
    if st.button("Start Study"):
        if participant.strip():
            st.session_state.participant = participant.strip()
            st.session_state.started = True
            st.session_state.trials = random.sample(
                [(i, t) for i in range(len(DATA)) for t in ["table","bar","line"]], 36
            )
            st.session_state.trial_index = 0
            st.session_state.results = []
            st.session_state.start_time = time.perf_counter()
            st.rerun()
        else:
            st.warning("Enter an anonymous participant ID.")
    st.info("Do not enter names, phone numbers, email addresses, or other identifying information.")
    st.stop()

idx = st.session_state.trial_index
if idx >= len(st.session_state.trials):
    results = pd.DataFrame(st.session_state.results)
    out = Path("results")
    out.mkdir(exist_ok=True)
    file_name = out / f"participant_{st.session_state.participant}.csv"
    results.to_csv(file_name, index=False)

    st.success("Study completed.")
    st.write(f"Accuracy: {results.correct.mean()*100:.1f}%")
    st.write(f"Mean response time: {results.response_time_sec.mean():.2f} s")
    st.write(f"Mean confidence: {results.confidence.mean():.2f}/5")
    st.download_button("Download your results", results.to_csv(index=False), file_name=file_name.name)
    if st.button("Start a new study"):
        reset_study()
    st.stop()

item_index, chart_type = st.session_state.trials[idx]
item = DATA[item_index]

st.progress(idx / len(st.session_state.trials))
st.caption(f"Trial {idx+1} of {len(st.session_state.trials)}")

if chart_type == "table":
    st.dataframe(make_table(item), hide_index=True, use_container_width=True)
elif chart_type in ["bar","line"]:
    st.pyplot(draw_chart(item, chart_type), clear_figure=True)

st.subheader(item["question"])

options = OPTIONS[item["task"]]
answer = st.radio("Select one answer:", options, key=f"answer_{idx}")
confidence = st.slider("How confident are you?", 1, 5, 3, key=f"confidence_{idx}")

if st.button("Submit Answer", type="primary"):
    response_time = time.perf_counter() - st.session_state.start_time
    correct = str(answer).strip().lower() == str(item["answer"]).strip().lower()
    st.session_state.results.append({
        "participant_id": st.session_state.participant,
        "trial": idx + 1,
        "data_display": chart_type,
        "task_type": item["task"],
        "question": item["question"],
        "answer": answer,
        "correct_answer": item["answer"],
        "correct": int(correct),
        "response_time_sec": round(response_time, 3),
        "confidence": confidence
    })
    st.session_state.trial_index += 1
    st.session_state.start_time = time.perf_counter()
    st.rerun()
