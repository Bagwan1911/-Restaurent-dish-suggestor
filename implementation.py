import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import ollama
import uuid
from datetime import datetime
from fpdf import FPDF


# ---------------- PDF INVOICE FUNCTION ----------------

def generate_invoice_pdf(
dish,
roti,
rice,
qty,
bill
):

    invoice_no=str(
    uuid.uuid4()
    )[:8].upper()

    date_time=datetime.now().strftime(
    "%d-%m-%Y %H:%M"
    )


    pdf=FPDF()
    pdf.add_page()

    pdf.set_font(
    "Arial",
    "B",
    16
    )

    pdf.cell(
    200,
    10,
    txt="Restaurant Invoice",
    ln=True,
    align="C"
    )

    pdf.ln(10)

    pdf.set_font(
    "Arial",
    size=12
    )


    pdf.cell(
    200,
    10,
    txt=f"Invoice No: {invoice_no}",
    ln=True
    )

    pdf.cell(
    200,
    10,
    txt=f"Date: {date_time}",
    ln=True
    )


    pdf.ln(5)

    pdf.cell(
    200,
    10,
    txt=f"Sabji: {dish}",
    ln=True
    )

    pdf.cell(
    200,
    10,
    txt=f"2 Rotis: {roti}",
    ln=True
    )

    pdf.cell(
    200,
    10,
    txt=f"Rice: {rice}",
    ln=True
    )

    pdf.cell(
    200,
    10,
    txt=f"Quantity: {qty}",
    ln=True
    )

    pdf.cell(
    200,
    10,
    txt=f"Total Bill: Rs {bill}",
    ln=True
    )


    pdf.ln(20)

    pdf.cell(
    200,
    10,
    txt="Thank You Visit Again",
    ln=True,
    align="C"
    )


    filename=f"invoice_{invoice_no}.pdf"

    pdf.output(
    filename
    )

    return filename



# ---------------- LOAD DATA ----------------

veg_menu=pd.read_csv(
"veg_menu.csv"
)

nonveg_menu=pd.read_csv(
"nonveg_menu.csv"
)

extras_menu=pd.read_csv(
"extras_menu.csv"
)


veg_menu.columns=veg_menu.columns.str.strip()
nonveg_menu.columns=nonveg_menu.columns.str.strip()
extras_menu.columns=extras_menu.columns.str.strip()



# ---------------- USER INPUT ----------------

food_type=input(
"Veg or Non-Veg: "
).lower()

spice=input(
"Spice Level (High/Medium/Low): "
).capitalize()

budget=int(
input("Enter Budget: ")
)



# ---------------- FILTER ----------------

if food_type=="veg":

    filtered=veg_menu[
    veg_menu["Spiciness"]==spice
    ]


elif food_type=="nonveg":

    filtered=nonveg_menu[
    nonveg_menu["Spiciness"]==spice
    ]


else:
    print("Wrong Input")
    exit()



# ---------------- COMBO GENERATOR ----------------

meal_combos=[]


roti_items=extras_menu[
extras_menu["dishname"].str.contains(
"Roti|Naan|Paratha",
case=False
)
]


rice_items=extras_menu[
extras_menu["dishname"].str.contains(
"Rice|Pulao",
case=False
)
]



dish_options=filtered.sort_values(
by="Price"
).head(5)



for _,dish in dish_options.iterrows():

    combo_count=0

    for _,roti in roti_items.iterrows():

        for _,rice in rice_items.iterrows():

            total=(
            dish["Price"]
            +(2*roti["Price"])
            +rice["Price"]
            )


            if total<=budget:

                meal_combos.append({

                "Sabji":
                dish["dishname"],

                "2 Rotis":
                roti["dishname"],

                "Rice":
                rice["dishname"],

                "Total Bill":
                total

                })

                combo_count+=1


            if combo_count==2:
                break

        if combo_count==2:
            break



combo_menu=pd.DataFrame(
meal_combos
).drop_duplicates()



if combo_menu.empty:

    print(
    "No meal combos possible"
    )

    exit()



print("\nRecommended Full Meal Combos\n")

print(
combo_menu.to_string(
index=False
)
)



# ---------------- TEXT CHUNKS ----------------

menu_text=[]


for _,row in combo_menu.iterrows():

    text=f"""
Meal Combo:
Sabji: {row['Sabji']}
2 Rotis: {row['2 Rotis']}
Rice: {row['Rice']}
Total Bill: {row['Total Bill']} rupees
"""

    menu_text.append(
    text
    )



# ---------------- EMBEDDINGS ----------------

model=SentenceTransformer(
"all-MiniLM-L6-v2"
)


menu_embeddings=model.encode(
menu_text
)

menu_embeddings=np.array(
menu_embeddings
).astype("float32")



if len(
menu_embeddings.shape
)==1:

    menu_embeddings=np.expand_dims(
    menu_embeddings,
    axis=0
    )



print(
"Embedding Shape:",
menu_embeddings.shape
)



# ---------------- FAISS ----------------

dimension=menu_embeddings.shape[1]


index=faiss.IndexFlatL2(
dimension
)

index.add(
menu_embeddings
)


print(
"Vectors Stored:",
index.ntotal
)



# ---------------- RETRIEVAL ----------------

query=f"""
Suggest best full meal combo
for {food_type}
with {spice} spice
under {budget}
"""


query_embedding=model.encode(
[query]
).astype("float32")


D,I=index.search(
query_embedding,
3
)



retrieved_combos=combo_menu.iloc[
I[0]
]



print(
"\nTop Retrieved Meal Combos\n"
)


for _,row in retrieved_combos.iterrows():

    print(
f"""
Sabji: {row['Sabji']}
2 Rotis: {row['2 Rotis']}
Rice: {row['Rice']}
Total Bill: {row['Total Bill']}
-------------------------
"""
    )



# ---------------- LLM SUGGESTIONS ----------------

context=""


for _,row in retrieved_combos.iterrows():

    context+=f"""
Sabji: {row['Sabji']}
2 Rotis: {row['2 Rotis']}
Rice: {row['Rice']}
Total Bill: {row['Total Bill']}
"""



prompt=f"""
You are a restaurant assistant.

User preferences:
Food Type: {food_type}
Spice Level: {spice}
Budget: {budget}

Retrieved meal combos:
{context}

Give exactly 3 suggestions:

1. Best Value Meal
2. Premium Choice
3. Budget Friendly Choice
"""


response=ollama.chat(
model="llama3",
messages=[
{
"role":"user",
"content":prompt
}
]
)


print(
"\n----- AI MEAL SUGGESTIONS -----\n"
)

print(
response["message"]["content"]
)



# ---------------- CHOOSE COMBO ----------------

choice=int(
input(
"\nSelect Combo (1/2/3): "
)
)


selected_combo=retrieved_combos.iloc[
choice-1
]



print(
f"""
You Selected

Sabji: {selected_combo['Sabji']}
2 Rotis: {selected_combo['2 Rotis']}
Rice: {selected_combo['Rice']}
Combo Price: ₹{selected_combo['Total Bill']}
"""
)



# ---------------- ORDER LOOP ----------------

while True:

    qty=int(
    input(
    "Enter Quantity of Meals: "
    )
    )


    final_bill=(
    selected_combo["Total Bill"]*qty
    )



    print(
"\n------ INVOICE PREVIEW ------"
    )


    print(
    "Sabji:",
    selected_combo["Sabji"]
    )

    print(
    "2 Rotis:",
    selected_combo["2 Rotis"]
    )

    print(
    "Rice:",
    selected_combo["Rice"]
    )

    print(
    "Quantity:",
    qty
    )

    print(
    "Payable Amount: ₹",
    final_bill
    )



    confirm=input(
    "\nPlace Order? yes/no: "
    ).lower()



    if confirm=="yes":

        print(
"\n===== ORDER PLACED SUCCESSFULLY =====\n"
        )


        print(
f"""
----------- FINAL BILL -----------

Meal:
{selected_combo['Sabji']}

Bread:
2 {selected_combo['2 Rotis']}

Rice:
{selected_combo['Rice']}

Quantity:
{qty}

Total Payable:
₹{final_bill}

Thank You Visit Again
"""
        )



        invoice_file=generate_invoice_pdf(
        selected_combo["Sabji"],
        selected_combo["2 Rotis"],
        selected_combo["Rice"],
        qty,
        final_bill
        )


        print(
f"Invoice Generated: {invoice_file}"
        )

        break



    elif confirm=="no":

        print(
        "\nEditing Order...\n"
        )

        continue


    else:

        print(
        "Invalid Input"
        )