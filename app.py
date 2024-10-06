import pandas as pd
import streamlit as st  # type: ignore

st.header('FIFA History Data.')
st.subheader('FIFA Stats Below!')
st.subheader('Select the year and the team')

# Load data from the CSV file
clean = pd.read_csv('data.csv')

# Select Year from unique years in the dataset
year = st.selectbox('Select Year', clean['Year'].sort_values().unique())

# Select Team from teams that played in the selected year
team = st.selectbox('Select Team', clean[clean['Year'] == year]['HomeTeam'].sort_values().unique())

def match_result(row, team):
    """Determine the match result for the selected team."""
    if row['HomeTeam'] == team:
        if row['HomeGoals'] > row['AwayGoals']:
            return 'Win'
        elif row['HomeGoals'] < row['AwayGoals']:
            return 'Loss'
        else:
            return 'Draw'
    elif row['AwayTeam'] == team:
        if row['AwayGoals'] > row['HomeGoals']:
            return 'Win'
        elif row['AwayGoals'] < row['HomeGoals']:
            return 'Loss'
        else:
            return 'Draw'
    else:
        return 'Not played'

# Filter data for the selected year
df = clean[clean['Year'] == year]
# Filter for matches involving the selected team
raw = df[(df['HomeTeam'] == team) | (df['AwayTeam'] == team)]

# Apply match_result function to get the result for each match
raw['result'] = raw.apply(lambda row: match_result(row, team), axis=1)

# Display the filtered DataFrame
st.dataframe(raw)

# Display statistics
st.write('Total Matches Played:', raw.shape[0])
st.write('Wins:', raw[raw['result'] == 'Win'].shape[0])
st.write('Losses:', raw[raw['result'] == 'Loss'].shape[0])
st.write('Draws:', raw[raw['result'] == 'Draw'].shape[0])
