import streamlit as st
import pandas as pd
import json
import joblib


path = "C:\\Users\\Adrian\\projecthacktiv8\\gradedchallenge5deployment\\gc5deployment\\"
# load file
with open('model_scaling.pkl', 'rb') as file_1:
  model_scaling = joblib.load(file_1)

with open('model_dt_pipe.pkl', 'rb') as file_10:
  dt_pipe = joblib.load(file_10)

with open('list_num_cols.txt', 'r') as file_17:
  num_features = json.load(file_17)

with open('model_selected_features.txt', 'r') as file_18:
  sel_features = json.load(file_18)

def run():
    # Membuat Form
    transaction_type_mapping = {
    0: 'PAYMENT',
    1: 'TRANSFER',
    2: 'CASH_OUT',
    3: 'DEBIT',
    4: 'CASH_IN'
}
    with st.form(key='form_credit_default_check'):
            step = st.number_input('step', min_value=0, max_value=1000000, value=5000, help='limit'), 
            type = st.selectbox('Predicted Transaction Type:', list(transaction_type_mapping.values()))
            amount = st.number_input('amount', min_value=0, max_value=10000000, value=100000, help='Umur'), 
            nameOrig = st.text_input('nameOrig', value = "C1231006815"), 
            oldbalanceOrg = st.number_input('oldbalanceOrg', min_value=0, max_value=10000000, value=100000), 
            newbalanceOrig = st.number_input('newbalanceOrig', min_value=0, max_value=10000000, value=100000), 
            nameDest = st.text_input('nameDest', value = "M1979787155"), 
            oldbalanceDest = st.number_input('oldbalanceDest', min_value=0, max_value=10000000, value=100000), 
            newbalanceDest = st.number_input('newbalanceDest', min_value=0, max_value=10000000, value=100000), 
            isFlaggedFraud = st.slider('isFlaggedFraud', 0,1,0), 


            submitted = st.form_submit_button('Predict')

    data_inf = {
              'step' : step[0],
              'type' : type,
              'amount' : amount,
              'nameOrig' : nameOrig[0],
              'oldbalanceOrg' : oldbalanceOrg[0],
              'newbalanceOrig' : newbalanceOrig[0],
              'nameDest' : nameDest[0],
              'oldbalanceDest' : oldbalanceDest[0],
              'newbalanceDest' : newbalanceDest[0],
              'isFlaggedFraud' : isFlaggedFraud[0],

    } #Key harus sama dengan column di dataset

    data_inf = pd.DataFrame([data_inf])
    st.dataframe(data_inf)

    print(data_inf)

    if submitted:
        data_inf_selected = data_inf[sel_features]
        # Feature Scaling 
        data_inf_selected[num_features] = model_scaling.transform(data_inf_selected[num_features])
        # Predict using Linear Regression
        y_pred_inf = dt_pipe.predict(data_inf_selected)
        st.write('# Fraud Prediction: ',str(int(y_pred_inf)))
        st.write('Jika 0 = Tidak Fraud')
        st.write('Jika 1 = Fraud')


if __name__ == '__main__':
    run()
