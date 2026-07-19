import streamlit as st
import json
import os
correct_password=st.secrets["app_password"]
password=st.text_input("enter password",type="password")
if password!=correct_password:
   st.stop()
DATA_FILE="tasks_data.json"
if "task" not in st.session_state:
   if os.path.exists(DATA_FILE):
      with open(DATA_FILE,"r") as f:
         st.session_state.task=json.load(f)
   else:
      st.session_state.task={}
def save_data():
   with open(DATA_FILE,"w") as f:
      json.dump(st.session_state.task,f)
if "date_confirmed" not in st.session_state:
  st.session_state.date_confirmed=False
if "next_clicked" not in st.session_state:
  st.session_state.next_clicked=False
name=st.text_input("Name:")
name_key=name.strip().lower()
st.write(f"Hello,{name}\n I am your mater,here to help you with your schedule tasks\n No need to worry when your mater buddy is here to make a clean proper schedule to help you.\nPlease click NEXT for the updating your schedule")
with st.sidebar:
   st.header("⚙️ Settings")
   bg_style=st.selectbox("Background style",["Solid color","Image URL"])
   if bg_style=="Solid color":
      bg_value=st.color_picker("Pick any color,\nclick on box","#FFFFFF")
   else:
      bg_value=st.text_input("Paste image URL")
   text_color=st.selectbox("Text color",["Black","White"])
   font_options={
      "Default":"sans-serif",
      "Serif":"Georgia,serif",
      "Monospace":"'Courier New',monospace",
      "Rounded":"'Trebuchet MS',sans-serif"
   }
   font_family=st.selectbox("Font Style",list(font_options.keys()))
   font_value=font_options[font_family] 
   if bg_style=="Solid color":
      bg_css_part=f"background-color:{bg_value};"
   else:
      bg_css_part=f"background-image:url('{bg_value}');background-size:cover;"
   full_css=f"""
   <style>
    .stApp{{
       {bg_css_part}
       color:{text_color};
       font-family:{font_value};
   }}
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div{{
       color:{text_color}! important;
   }}
    .stTextInput input, .stTextArea textarea{{
       color:black !important;
       background-color:white !important;
   }}
   </style>
   """
   if bg_style=="Image URL" and bg_value=="":
      st.info("Paste an image URL to apply it as background")
   else:
      st.markdown(full_css,unsafe_allow_html=True)                            
if st.button("Next"):
   st.session_state.next_clicked=True
if st.session_state.next_clicked:
   st.write(f"Lets schedule your task {name}")
   selected_date=st.date_input("Pick your Date")
   date_key=selected_date.isoformat()
   if name_key not in st.session_state.task:
      st.session_state.task[name_key]={}
   if date_key not in st.session_state.task[name_key]:
      st.session_state.task[name_key][date_key]=[]
   with st.form("add_task_form",clear_on_submit=True):
      newTask=st.text_input("Enter the Task:")
      submitted=st.form_submit_button("Add Task")
   if submitted:
      st.session_state.task[name_key][date_key].append({"text":newTask,"done":False,"note":""}) 
      save_data() 
   for index,t in enumerate(st.session_state.task[name_key][date_key]):
       checked=st.checkbox(t["text"],value=t["done"],key=f"check_{date_key}_{index}")
       if checked!=t["done"]:
         t["done"]=checked
         save_data()
       remove=st.button("🗑️Remove",key=f"remove_{date_key}_{index}")
       if remove:
         st.session_state.task[name_key][date_key].remove(t)
         save_data()
         st.rerun()
       with st.expander("➕ Note"):
         note_val=st.text_area("Note",value=t["note"],key=f"note_{date_key}_{index}")
         t["note"]=note_val
         save_data()
   done_count=0
   for t in st.session_state.task[name_key][date_key]:
       if t["done"]:
        done_count+=1
   total_count=len(st.session_state.task[name_key][date_key])
   st.write(f"{done_count}/{total_count}tasks done")
   st.write("✅ Done:")
   for t in st.session_state.task[name_key][date_key]:
      if t["done"]:
         st.write(t["text"])
   st.write("❌ Not Done:")
   for t in st.session_state.task[name_key][date_key]:
      if t["done"]==False:
         st.write(t["text"])

          
       
