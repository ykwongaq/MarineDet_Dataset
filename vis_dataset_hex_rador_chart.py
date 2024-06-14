import numpy as np
import plotly.graph_objects as go

def normalize(data):
    normalized_data = []
    for metric_values in zip(*data):
        min_val = min(metric_values)
        max_val = max(metric_values)
        normalized_metric = [(value - min_val) / (max_val - min_val) for value in metric_values]
        normalized_data.append(normalized_metric)
    return list(zip(*normalized_data))

def robust_scale(data):
    scaled_data = []
    for metric_values in zip(*data):
        Q1 = np.percentile(metric_values, 25)
        Q3 = np.percentile(metric_values, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        clipped_values = [max(min(value, upper_bound), lower_bound) for value in metric_values]
        min_val = min(clipped_values)
        max_val = max(clipped_values)
        normalized_metric = [(value - min_val) / (max_val - min_val) for value in clipped_values]
        scaled_data.append(normalized_metric)
    return list(zip(*scaled_data))
    
def example_data():
    data = {
        'metrics': ['Category', 'Image', 'Annotation', 'Text-Image', 'Avg Length'],
        'group_data': [
            ('MarineDet', [670, 14645, 5, 34752, 33]),
            ('URPC2018', [4, 3701, 2, 0, 0]),
            ('DUO', [4, 7782, 3, 0, 0]),
            ('SUIM', [8, 1500, 3, 0, 0]),
            ('MAS3K', [37, 3103, 5, 0, 0]),
            ('UIIS', [7, 4628, 3, 0, 0]),
            ('SEAMPD21', [37, 3103, 2, 0, 0]),
            ('Wildfish', [1000, 54459, 1, 0, 0]),
            ('FishNet', [17357, 94532, 3, 0, 0]),
            ('Wildfish++', [2348, 103034, 1, 72351, 45]),
        ]
    }
    return data

data = example_data()

metrics = data['metrics']
group_data = data['group_data']

# Extract the values to normalize
values = [group_values for _, group_values in group_data]

# Normalize the data
normalized_values = normalize(values)

fig = go.Figure()

for i, (group_name, _) in enumerate(group_data):
    fig.add_trace(go.Scatterpolar(
        r=normalized_values[i],
        theta=metrics,
        fill='toself',
        name=group_name
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        )),
    showlegend=True
)

fig.show()
