import streamlit as st #app interface
import sqlite3 #connects w/ database, allows for responses to be logged
import pandas as pd #library for data tables, analyzes data from database

st.title("2025 FRC Scouting 2.0")
st.write(
    "Input the match data here :D"
)

#set up database

conn = sqlite3.connect("MatchData.db") #creates database file from SQLite

cursor = conn.cursor() #allows to send commands to database (inserting info, collecting data, etc)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS MatchData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        

        Team_Number INTEGER,
        Alliance_Partner_1 INTEGER, 
        Alliance_Partner_2 INTEGER,
        Match_Number INTEGER,
        Match_Type TEXT, 

        Total_Match_Points INTEGER,
        Total_Ranking_Points INTEGER, 
        Total_Auto_Points INTEGER,
        Total_Teleop_Points INTEGER,
        
        
        Auto_Leave_Points INTEGER, 
        Number_Robots_Leave INTEGER, 
        Did_Team_Leave BOOLEAN, 
        Auto_Level_1_Coral INTEGER,
        Auto_Level_2_Coral INTEGER, 
        Auto_Level_3_Coral INTEGER, 
        Auto_Level_4_Coral INTEGER, 
        Auto_Net_Algae INTEGER,
        Auto_Processor_Algae INTEGER,
        Auto_Notes TEXT,

        
        Teleop_Level_1_Coral INTEGER, 
        Teleop_Level_2_Coral INTEGER, 
        Teleop_Level_3_Coral INTEGER, 
        Teleop_Level_4_Coral INTEGER, 
        Teleop_Net_Algae INTEGER,
        Teleop_Processor_Algae INTEGER, 
        Teleop_Cycles INTEGER,
        Teleop_Priority TEXT,
        Teleop_Notes TEXT,
        

        Total_Hang_Points INTEGER, 
        Barge_Zone BOOLEAN, 
        Shallow_Cage BOOLEAN, 
        Deep_Cage BOOLEAN, 
        Hang_Type TEXT,
        Hang_Consistency TEXT,
        Hang_Notes TEXT,

        
        Major_Fouls INTEGER, 
        Minor_Fouls INTEGER,
        
        
        Match_Result TEXT,
        Win_RP BOOLEAN,
        Tie_RP BOOLEAN,
        Auto_RP BOOLEAN, 
        Coral_RP BOOLEAN, 
        Barge_RP BOOLEAN, 

        
        Additional_Notes TEXT
        
        )
        """)

#create form
with st.form("Scouting Form"):
    #different inputs: st.text_input, st.number_input, st.selectbox, st.toggle (on/off switch), st.checkbox, st.radio, st.selectbox

    st.write ("Match Info")

    #text box created for team info
    Team_Number = st.number_input("Team Number", step=1)
    Alliance_Partner_1 = st.number_input ("Alliance Team 1 Number", step=1)
    Alliance_Partner_2 = st.number_input ("Alliance Team 2 Number", step=1)

#match info
    Match_Number = st.number_input ("Match Number", step=1)
    Match_Type = st.selectbox (
        "Match Type", 
        ["Qualification", "Practice", "Elimination"],
        )

    st.write ("Autonomous Data")

    Number_Robots_Leave = st.number_input ("Total # of Robots That Left During Auto", step=1)
    Did_Team_Leave = st.toggle ("Did team leave?") 
    Auto_Level_1_Coral = st.number_input ("How much level 1 coral?", step=1)
    Auto_Level_2_Coral = st.number_input ("How much level 2 coral?", step=1)
    Auto_Level_3_Coral = st.number_input ("How much level 3 coral?", step=1)
    Auto_Level_4_Coral = st.number_input ("How much level 4 coral?", step=1)
    Auto_Net_Algae = st.number_input ("How much net algae?", step=1)
    Auto_Processor_Algae = st.number_input ("How much processor algae?", step=1)
    Auto_Notes = st.text_input ("Any other notes?")

    st.write ("Teleop Data")

    Teleop_Level_1_Coral = st.number_input ("Level 1 coral?", step=1)
    Teleop_Level_2_Coral = st.number_input ("Level 2 coral?", step=1)
    Teleop_Level_3_Coral = st.number_input ("Level 3 coral?", step=1)
    Teleop_Level_4_Coral = st.number_input ("Level 4 coral?", step=1)
    Teleop_Net_Algae = st.number_input ("Net algae?", step=1)
    Teleop_Processor_Algae = st.number_input ("Processor algae?", step=1)
    Teleop_Cycles = st.number_input ("Cycle Count", step=1)
    Teleop_Priority = st.selectbox (
        "Teleop Priority",
        ["Coral", "Algae", "Defense", "Other"],
    )
    Teleop_Notes = st.text_input ("Any other notes? *If Other for the previous question, describe here.")

    st.write ("Hang Data")

    Hang_Type = st.selectbox (
        "Hang Type", 
        ["Barge Zone", "Shallow Cage", "Deep Cage"],
        )
    
    Hang_Consistency = st.selectbox (
        "Hang Consistency",
        ["Poor (0-40%)", "Average (40-70%)", "Consistent (70-90%)", "Extremely Consistent (90-100%)"],
    )
    Hang_Notes = st.text ("Any other notes?")

    st.write ("Fouls")

    Major_Fouls = st.number_input ("# of major fouls", step=1)
    Minor_Fouls = st.number_input ("# of minor fouls", step=1)

    st.write ("Ranking Point Data")

    Match_Result = st.selectbox (
        "Match Result",
        ["Win", "Loss", "Tie"],
    )
    Auto_RP = st.toggle ("Auto RP?")
    Coral_RP = st.toggle ("Coral RP?")
    Barge_RP = st.toggle ("Barge RP?")

    submitted = st.form_submit_button("Submit Match Data")

    if submitted:

        #set default variable values
        Total_Ranking_Points = 0
        Total_Auto_Points = 0
        Total_Teleop_Points = 0
        Auto_Leave_Points = 0
        Total_Hang_Points = 0
        

        #set variables dependent on other variables
        Auto_Leave_Points = 3 * Number_Robots_Leave
        Total_Auto_Points = Auto_Leave_Points + 3 * Auto_Level_1_Coral + 4 * Auto_Level_2_Coral + 6 * Auto_Level_3_Coral + 7 * Auto_Level_4_Coral + 4 * Auto_Net_Algae + 6 * Auto_Processor_Algae
        Total_Teleop_Points = 2 * Teleop_Level_1_Coral + 3 * Teleop_Level_2_Coral + 4 * Teleop_Level_3_Coral + 5 * Teleop_Level_4_Coral + 4 * Teleop_Net_Algae + 6 * Teleop_Processor_Algae
        Total_Match_Points = Total_Auto_Points + Total_Teleop_Points + Total_Hang_Points
        Total_Hang_Points = 2 * Barge_Zone + 6 * Shallow_Cage + 12 * Deep_Cage
        
        
        if Win_RP:
            Total_Ranking_Points +=3 #if they win, add 3 ranking points



        #insert data into database
        cursor.execute("""
        INSERT INTO MatchData (
            Team_Number,
            Alliance_Partner_1,
            Alliance_Partner_2,
            Match_Number,
            Match_Type,
            Total_Match_Points,
            Total_Ranking_Points,
            Total_Auto_Points,
            Total_Teleop_Points,
            Auto_Leave_Points,
            Number_Robots_Leave,
            Did_Team_Leave,
            Auto_Level_1_Coral,
            Auto_Level_2_Coral,
            Auto_Level_3_Coral,
            Auto_Level_4_Coral,
            Auto_Net_Algae,
            Auto_Processor_Algae,
            Auto_Notes,
            Teleop_Level_1_Coral,
            Teleop_Level_2_Coral,
            Teleop_Level_3_Coral,
            Teleop_Level_4_Coral,
            Teleop_Net_Algae,
            Teleop_Processor_Algae,
            Teleop_Cycles,
            Teleop_Priority,
            Teleop_Notes,
            Total_Hang_Points,
            Barge_Zone,
            Shallow_Cage,
            Deep_Cage,
            Hang_Type,
            Hang_Consistency,
            Hang_Notes,
            Major_Fouls,
            Minor_Fouls,
            Match_Result,
            Win_RP,
            Tie_RP,
            Auto_RP,
            Coral_RP,
            Barge_RP,
            Additional_Notes
        )
        """)
        #saves data to database
        conn.commit()
        #submit message
        st.success("Your data has been saved.")


        #turn results into dataframe
        df = pd.read_sql_query(
            "SELECT * FROM responses",
            conn
        )
        #display data table
        st.dataframe(df)