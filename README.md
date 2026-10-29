# Data Visualization and Decision-Making Study

## Purpose
A reproducible experimental prototype for comparing **tables, bar charts, and line graphs** on:
- accuracy
- response time
- confidence
- task-specific errors

## Experimental design
The prototype uses a within-participant design. Each participant completes 36 randomized trials:
- 12 data questions
- each question shown as a table, bar chart, and line graph
- task types: exact-value retrieval, category comparison, and trend detection

The application records:
`participant_id, trial, data_display, task_type, question, answer, correct_answer, correct, response_time_sec, confidence`

## Run
1. Install Python 3.10 or later.
2. Open a terminal in this folder.
3. Run:
   `pip install -r requirements.txt`
4. Start:
   `streamlit run main.py`
5. Complete the study using an anonymous participant code.
6. Participant files are saved in `results/`.
7. After collecting data from multiple participants, run:
   `python analyze_results.py`

## Important research note
Do not claim experimental findings before collecting and analyzing participant data. The paper should report actual sample size, means, standard deviations, statistical tests, and p-values only after the study is conducted.

## Suggested IEEE paper use
The complete source code is supplementary material. In the main paper, include a short algorithm/code listing rather than the entire application source.
