import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
from fpdf import FPDF


# ---------------- PAGE ----------------

st.set_page_config(
page_title="AI Restaurant Ordering",
layout="wide"
)

st.title("🍽 AI Restaurant Ordering System")


# ---------------- INVOICE NUMBER ----------------

invoice_no="INV-"+str(
uuid.uuid4()
)[:8].upper()



# ---------------- PDF FUNCTION ----------------

def generate_invoice_pdf(
dish,
roti,
rice,
qty,
bill
):

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


    rows=[
    f"Invoice Number: {invoice_no}",
    f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
    "",
    f"Sabji: {dish}",
    f"2 Rotis: {roti}",
    f"Rice: {rice}",
    f"Quantity: {qty}",
    f"Total Bill: Rs {bill}",
    "",
    "Thank You Visit Again"
    ]


    for row in rows:

        pdf.cell(
        200,
        10,
        txt=str(row),
        ln=True
        )


    filename="invoice.pdf"

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



# ---------------- INPUTS ----------------

food_type=st.selectbox(
"Food Type",
["veg","nonveg"]
)

spice=st.selectbox(
"Spice Level",
["Low","Medium","High"]
)

budget=st.number_input(
"Budget",
min_value=200,
value=500
)



# ---------------- SHOW COMBOS ----------------

if st.button(
"Show Suggested Combos"
):

    if food_type=="veg":

        filtered=veg_menu[
        veg_menu["Spiciness"]==spice
        ]

    else:

        filtered=nonveg_menu[
        nonveg_menu["Spiciness"]==spice
        ]



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


    meal_combos=[]


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

                    "Price":
                    total

                    })

                    combo_count+=1


                if combo_count==2:
                    break

            if combo_count==2:
                break



    st.session_state.combo_menu=pd.DataFrame(
    meal_combos
    ).drop_duplicates()



# ---------------- DISPLAY COMBOS ----------------

if "combo_menu" in st.session_state:

    combo_menu=st.session_state.combo_menu


    st.subheader(
    "🍛 Suggested Meal Combos"
    )

    st.dataframe(
    combo_menu
    )



    combo_options=[]

    for i,row in combo_menu.iterrows():

        combo_options.append(
f"{i+1}. {row['Sabji']} + 2 {row['2 Rotis']} + {row['Rice']} (₹{row['Price']})"
        )



    selected_combo_text=st.selectbox(
    "Select Combo",
    combo_options
    )



    selected_index=combo_options.index(
    selected_combo_text
    )


    selected_combo=combo_menu.iloc[
    selected_index
    ]



    qty=st.number_input(
    "Quantity",
    min_value=1,
    value=1
    )



    if st.button(
    "Generate Invoice"
    ):

        bill=(
        selected_combo["Price"]*qty
        )

        st.session_state.bill=bill
        st.session_state.qty=qty
        st.session_state.selected_combo=selected_combo



# ---------------- INVOICE ----------------

if "bill" in st.session_state:

    combo=st.session_state.selected_combo

    st.subheader(
    "🧾 Invoice Preview"
    )

    st.write(
    f"Invoice Number: {invoice_no}"
    )

    st.write(
    f"Sabji: {combo['Sabji']}"
    )

    st.write(
    f"2 Rotis: {combo['2 Rotis']}"
    )

    st.write(
    f"Rice: {combo['Rice']}"
    )

    st.write(
    f"Quantity: {st.session_state.qty}"
    )


    st.success(
f"Total Bill ₹{st.session_state.bill}"
    )



    decision=st.radio(
    "Confirm Order",
    [
    "Yes Place Order",
    "No Edit Order"
    ]
    )



    if decision=="Yes Place Order":

        if st.button(
        "Place Order"
        ):

            st.balloons()

            st.success(
            "✅ Order Placed Successfully"
            )


            st.subheader(
            "Final Bill"
            )

            st.write(
f"""
Invoice Number:
{invoice_no}

Meal:
{combo['Sabji']}

Bread:
2 {combo['2 Rotis']}

Rice:
{combo['Rice']}

Quantity:
{st.session_state.qty}

Payable Amount:
₹{st.session_state.bill}
"""
            )



            pdf_file=generate_invoice_pdf(
            combo["Sabji"],
            combo["2 Rotis"],
            combo["Rice"],
            st.session_state.qty,
            st.session_state.bill
            )


            with open(
            pdf_file,
            "rb"
            ) as file:

                st.download_button(
                label="📄 Download Invoice PDF",
                data=file,
                file_name=f"{invoice_no}.pdf",
                mime="application/pdf"
                )



    elif decision=="No Edit Order":

        st.warning(
        "Edit combo above and regenerate invoice."
        )