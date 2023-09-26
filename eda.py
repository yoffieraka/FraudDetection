import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image


def run():
    # Membuat Title
    st.title('Fraud Detection Model')

    # Membuat Sub Header
    st.subheader('Membuat EDA untuk Fraud Detection')

    # #Menambahkan Gambar
    # image = Image.open('cc.jpg')
    # st.image(image, caption='Black Card')

    #Menambahkan Deskripsi
    st.write('Page ini dibuat oleh **Syechrifanka Yoffi Adrian**')

    #Load Data Frame
    data = pd.read_csv('Fraud.csv')

    #Membuat Barplot
    st.subheader('*Distribusi data type transaksi, dan jenis penipuan*')
    sns.set(style="whitegrid")
    # Define the number of rows and columns for subplots
    categorical_cols = ['type','isFraud','isFlaggedFraud']
    num_rows = 1
    num_cols = len(categorical_cols)
    # Create a figure and axis for subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 6))
    # Flatten the axes array for easy iteration
    axes = axes.flatten()
    # Iterate through categorical columns
    for i, col in enumerate(categorical_cols):
        if col == "isFraud" or col == "isFlaggedFraud":
            # Use a logarithmic scale for the Y-axis
            sns.countplot(data=data, x=col, ax=axes[i], palette={0: "blue", 1: "red"})
            axes[i].set_yscale("log") #Dikarenakan data yang imbalance, maka dilakukan pengskalaan logaritmik jika tidak value 1 tidak akan terlihat pada isFraud dan isFlaggedFraud
        else:
            sns.countplot(data=data, x=col, ax=axes[i], palette="Set3")
        axes[i].set_title(col)
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("Count")
    # Adjust layout
    plt.tight_layout()
    st.pyplot(fig)
    st.write('Berdasarkan transaksi yang dilakukan oleh para pengguna, Transaksi paling banyak dilakukan dengan cara penarikan uang yang kedua ialah cash out, untuk data penipuannya dari plot, data paling banyak adalah ada yang aman dibandingkan dengan data penipu, berdasarkan hasilnya ini dapat membuktikan bahwa data ini imbalance')

    st.subheader('*Distribusi Jumlah Penipuan dengan Tipe Transaksinya*')
    # Convert the 'type' column to categorical
    data['type'] = data['type'].astype('category')
    # Create a selection box for transaction type
    pilihan = st.selectbox('Pilih Transaction Type:', data['type'].cat.categories)
    # Filter the data based on the selected transaction type
    filtered_data = data[data['type'] == pilihan]
    # Create the count plot
    fig = plt.figure(figsize=(10, 6))
    sns.countplot(data=filtered_data, x='type', hue="isFraud", palette="Set1")
    # Set labels and title
    plt.xlabel("Transaction Type")
    plt.ylabel("Count")
    plt.title("Distribution of Fraud vs. Transaction Type")
    st.pyplot(fig)
    st.write('Dikarenakan data yang imbalance yaitu lebih banyak data yang tidak fraud maka data fraud sulit terlihat, untuk lebih detailnya ada pada plot setelah ini.')

    st.subheader('*Jumlah Penipuan dengan Tipe Transaksinya*')
    # Count the occurrences of each transaction type for fraud cases
    fraud_transaction_counts = data[data['isFraud'] == 1]['type'].value_counts()
    # Plot the counts
    fig = plt.figure(figsize=(10, 6))
    fraud_transaction_counts.plot(kind='bar', color='orange')
    plt.title('Transaction Types for Fraud Cases')
    plt.xlabel('Transaction Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.write('Dapat dilihat jumlah penipuan terjadi paling banyak hanya pada Penarikan uang dan transfer dimana pihak perusahaan harus memberikan perhatian yang lebih terhadap kedua transaksi ini')

    st.subheader('*Perbandingan data tidak Fraud dengan Fraud*')
    # pie plot for the value count
    fig = plt.figure(figsize=(10, 6))
    plt.pie(data.isFraud.value_counts(),explode=[0.1, 0], 
            labels=['No Fraud', 'Fraud'], shadow=True, autopct='%1.1f%%')
    st.pyplot(fig)
    st.write('Jumlah data sulit ditampilkan dengan sesungguhnya dikarenakan data yang sangat tidak seimbang dimana data Fraud hanya 0.1\% dari keseluruhan data')

    # #Membuat Boxplot Berdasarkan Inputan User
    # st.write('#### Boxplot Berdasarkan Input User')
    # pilihan = st.selectbox('Pilih Column:', ('limit_balance','age','bill_amt_1','bill_amt_2','bill_amt_3','bill_amt_4','bill_amt_5','bill_amt_6','pay_amt_1','pay_amt_2','pay_amt_3','pay_amt_4','pay_amt_5','pay_amt_6'))
    # fig = plt.figure(figsize = (15,5))
    # sns.boxplot(data=data, x=data[pilihan], palette="Set3")
    # st.pyplot(fig)

    # #Membuat Pie Chart default payment next month
    # default_counts = data['default_payment_next_month'].value_counts()
    # st.write('#### Histogram of Rating')
    # fig = plt.figure(figsize=(6, 6))
    # sns.set(style="whitegrid")
    # plt.pie(default_counts, labels=default_counts.index, autopct='%1.1f%%', startangle=140, colors=['skyblue', 'lightcoral'])
    # plt.title('Distribution of Default Payment')
    # st.pyplot(fig)
    # st.markdown('Berdasarkan Pie Chart Diatas, dapat disimpulkan bahwa terdapat 21,4% pengguna kartu kredit yang gagal dalam pembayaran kartu kredit serta 78,6% pengguna kartu kredit yang pembayarannya lancar')


if __name__ == '__main__':
    run()