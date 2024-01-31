import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from string import punctuation
import unicodedata
nltk.download('stopwords')
stemmer = SnowballStemmer('english')
nltk.download('punkt')
stop_words = set(stopwords.words('english')) 

import pickle
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

with open('model.pkl', 'rb') as archivo_modelo:
    classifier = pickle.load(archivo_modelo)
 
with open('vectorizer.pkl', 'rb') as archivo_vectorizador:
    vec = pickle.load(archivo_vectorizador)

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def fast_preproc(text):
  text = text.lower()
  text = ''.join(c for c in text if not c.isdigit())
  text = ''.join(c for c in text if c not in punctuation)
  text = remove_accents(text)
  words = word_tokenize(text)
  words = [stemmer.stem(word) for word in words]  
  words = [word for word in words if not word in stop_words] 
  try:
    text = " ".join(str(word) for word in words)
  except Exception as e:
    print(e)
    pass
  return text
 
def generate_button_click():
    opinion = t.get("1.0", "end-1c")  # Obtener el texto ingresado por el usuario
    opinion_preprocesada = fast_preproc(str(opinion))
    trans_opinion = vec.transform([opinion_preprocesada])
    resultado_prediccion = classifier.predict(trans_opinion)
    proba_resultado = classifier.predict_proba(trans_opinion)[0]
    sorted_indices = proba_resultado.argsort()[::-1][:5]

    result_box.delete("1.0", "end")
    result_box.insert("end", "The 5 main routes:\n\n")

    for idx in sorted_indices:
        clase = classifier.classes_[idx]
        probabilidad = proba_resultado[idx]
        line = f"Route: {clase}\nProbability: {probabilidad*100:.2f}%\n\n"
        if idx == sorted_indices[0]:
            result_box.insert("end", line, "green")
        else:
            result_box.insert("end", line)
    result_box.tag_configure("green", foreground="green")

if __name__ == "__main__":
    app = tk.Tk()

    app.geometry("425x550")
    app.config(background="#b6ccd8")
    app.title("Category Product Assistant")

    frame_ppal = ttk.Frame(app)
    frame_ppal = tk.Label(frame_ppal, background="#b6ccd8")
    frame_ppal.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

    frame_titulo = ttk.Frame(app)
    frame_titulo.grid(column=0, row=0, columnspan=3, pady=10)

    titulo_label = ttk.Label(frame_titulo, text="PriceRunner Assistant", font=("Segoe UI", 20, "bold"),background="#b6ccd8", foreground="#3b3c3d")
    titulo_label.grid(column=0, row=0)

    frame_separador = ttk.Frame(app, height=2, relief="sunken")
    frame_separador.grid(column=0, row=1, columnspan=3, sticky="ew")

    ttk.Label(app, text="Enter the product description:", font=("Segoe UI", 14), background="#b6ccd8", foreground="#3b3c3d").grid(
        column=0, row=2, padx=10, pady=25, columnspan=3)

    t = tk.Text(app, width=50, height=5)
    t.grid(column=0, row=3, padx=10, pady=10, columnspan=3)

    generate_button = tk.Button(app, text="Category Product", font=("Segoe UI", 14), background="#00668c", foreground="white", command=generate_button_click)
    generate_button.grid(column=1, row=4, pady=10)

    result_box = tk.Text(app, width=50, height=10)
    result_box.grid(column=0, row=5, padx=10, pady=10, columnspan=3)

    logo_path = "logo.png"
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((100,30), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)

    logo_label = ttk.Label(app, image=logo_photo, background="#b6ccd8")
    logo_label.grid(column=1, row=6, pady=10)

    app.mainloop()