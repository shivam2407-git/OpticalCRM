import streamlit as st
import sqlite3
import pandas as pd
from pdf_generator import generate_pdf

# ==========================
# PAGE SETTINGS
# ==========================

st.set_page_config(page_title="Optical CRM", page_icon="👓", layout="wide")

# ==========================
# DATABASE
# ==========================

conn = sqlite3.connect("optical_store.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
mobile TEXT UNIQUE,
address TEXT,
age INTEGER,
dob TEXT,
right_sph TEXT,
right_cyl TEXT,
right_axis TEXT,
left_sph TEXT,
left_cyl TEXT,
left_axis TEXT,
pd TEXT,
notes TEXT
)
""")

conn.commit()

# ==========================
# SIDEBAR
# ==========================

menu = st.sidebar.radio(
    "👓 Optical CRM",
    [
        "Dashboard",
        "Add Customer",
        "Search Customer",
        "Update Customer",
        "Delete Customer",
        "All Customers",
        "Birthday Customers",
        "Generate PDF"
    ],
)

# ==========================
# DASHBOARD
# ==========================

if menu == "Dashboard":

    st.title("📊 Dashboard")

    total_customers = cursor.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👥 Total Customers", total_customers)

    with col2:
        st.metric("💾 Database", "Active")

    with col3:
        st.metric("👓 Store", "Optical CRM")

    st.subheader("🔍 Quick Search")

    quick_mobile = st.text_input("Enter Mobile Number")

    if st.button("Quick Search"):

        cursor.execute(
            "SELECT * FROM customers WHERE mobile=?",
            (quick_mobile,)
        )

        data = cursor.fetchone()

        if data:
            st.success("Customer Found")
            st.write("👤 Name:", data[1])
            st.write("📱 Mobile:", data[2])
            st.write("📍 Address:", data[3])
        else:
            st.error("Customer Not Found")

# ==========================
# ADD CUSTOMER
# ==========================

elif menu == "Add Customer":

    st.title("➕ Add Customer")

    name = st.text_input("Customer Name")
    mobile = st.text_input("Mobile Number")
    address = st.text_area("Address")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1)

    with col2:
        from datetime import date

    dob = st.date_input(
        "Date of Birth",
        min_value=date(1950, 1, 1),
        max_value=date.today()
    )
    dob = dob.strftime("%d-%m-%Y")

    st.subheader("👁 Right Eye")

    right_sph = st.text_input("SPH")

    right_cyl = st.text_input("CYL")

    right_axis = st.text_input("AXIS")

    st.subheader("👁 Left Eye")

    left_sph = st.text_input("Left SPH")

    left_cyl = st.text_input("Left CYL")

    left_axis = st.text_input("Left AXIS")

    pupil_distance = st.text_input("PD")

    notes = st.text_area("Notes")

    if st.button("Save Customer"):

        try:

            cursor.execute(
                """
                INSERT INTO customers
                (
                name,mobile,address,age,dob,
                right_sph,right_cyl,right_axis,
                left_sph,left_cyl,left_axis,
                pd,notes
                )
                VALUES
                (?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    name,
                    mobile,
                    address,
                    age,
                    dob,
                    right_sph,
                    right_cyl,
                    right_axis,
                    left_sph,
                    left_cyl,
                    left_axis,
                    pupil_distance,
                    notes,
                ),
            )

            conn.commit()

            st.success("Customer Saved Successfully")

        except Exception as e:

            st.error(str(e))

# ==========================
# SEARCH CUSTOMER
# ==========================

elif menu == "Search Customer":

    st.title("🔍 Search Customer")

    search_type = st.selectbox(
        "Search By",
        ["Mobile", "Name"]
    )

    search_value = st.text_input(
        f"Enter {search_type}"
    )

    if st.button("Search"):

        if search_type == "Mobile":

            cursor.execute(
                "SELECT * FROM customers WHERE mobile=?",
                (search_value,)
            )

        else:

            cursor.execute(
                "SELECT * FROM customers WHERE name LIKE ?",
                (f"%{search_value}%",)
            )

        results = cursor.fetchall()
        
        st.session_state["results"] = results

    if "results" in st.session_state:

        results = st.session_state["results"]

        if results:

            for data in results:

                st.write("---")
                st.write("👤 Name:", data[1])
                st.write("📱 Mobile:", data[2])
                st.write("📍 Address:", data[3])
                st.write("🎂 DOB:", data[5])
                st.write("👓 Right SPH:", data[6])
                st.write("👓 Left SPH:", data[9])
                st.write("📏 PD:", data[12])

                if st.button(
                    f"📄 Generate PDF {data[0]}",
                    key=f"pdf_{data[0]}"
                ):

                    filename = generate_pdf(data)

                    st.success(
                        f"PDF Created: {filename}"
                    )

                    with open(filename, "rb") as file:

                        st.download_button(
                            label="⬇ Download Prescription",
                            data=file.read(),
                            file_name=filename,
                            mime="application/pdf",
                            key=f"download_{data[0]}"
                        )

        else:

            st.error("Customer Not Found")
            
# ==========================
# UPDATE CUSTOMER
# ==========================

elif menu == "Update Customer":

    st.title("✏️ Update Customer")

    mobile = st.text_input("Customer Mobile Number")

    new_name = st.text_input("New Name")

    new_address = st.text_input("New Address")

    new_age = st.number_input("New Age", min_value=1)

    if st.button("Update Customer"):

        cursor.execute(
            """
            UPDATE customers
            SET
            name=?,
            address=?,
            age=?
            WHERE mobile=?
            """,
            (new_name, new_address, new_age, mobile),
        )

        conn.commit()

        st.success("Customer Updated")

# ==========================
# DELETE CUSTOMER
# ==========================

elif menu == "Delete Customer":

    st.title("🗑 Delete Customer")

    delete_type = st.selectbox(
        "Delete By",
        ["Mobile", "Name"]
    )

    delete_value = st.text_input(
        f"Enter {delete_type}"
    )

    if st.button("Delete Customer"):

        if delete_type == "Mobile":

            cursor.execute(
                """
                DELETE FROM customers
                WHERE mobile=?
                """,
                (delete_value,)
            )

        else:

            cursor.execute(
                """
                DELETE FROM customers
                WHERE name=?
                """,
                (delete_value,)
            )

        conn.commit()

        st.success("Customer Deleted Successfully")

# ==========================
# ALL CUSTOMERS
# ==========================

elif menu == "All Customers":

    import io

    st.title("📋 All Customers")

    df = pd.read_sql_query(
        """
        SELECT *
        FROM customers
        ORDER BY id DESC
        """,
        conn,
    )

    st.dataframe(df, use_container_width=True, hide_index=True)

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:

        df.to_excel(writer, index=False)

    st.download_button(
        label="📊 Export Customers to Excel",
        data=excel_buffer.getvalue(),
        file_name="customers.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    with open("optical_store.db", "rb") as file:

        st.download_button(
            label="📁 Download Database Backup",
            data=file,
            file_name="optical_store_backup.db",
        )

# "Birthday Customers"

elif menu == "Birthday Customers":

    from datetime import datetime

    st.title("🎂 Birthday Customers")

    today = datetime.now().strftime("%d-%m")

    cursor.execute("""
    SELECT *
    FROM customers
    """)

    customers = cursor.fetchall()

    found = False

    for customer in customers:

        dob = customer[5]

        if dob and dob[:5] == today:

            found = True

            st.success(
                f"{customer[1]} - {customer[2]}"
            )

    if not found:

        st.info(
            "No birthdays today"
        )
        
# ==========================
# GENERATE PDF
# ==========================

elif menu == "Generate PDF":

    st.title("📄 Generate PDF")

    mobile = st.text_input("Enter Mobile Number")

    if st.button("Generate"):

        cursor.execute(
            "SELECT * FROM customers WHERE mobile=?",
            (mobile,)
        )

        data = cursor.fetchone()

        if data:

            filename = generate_pdf(data)

            st.success(f"PDF Created: {filename}")

            with open(filename, "rb") as file:

                st.download_button(
                    "⬇ Download PDF",
                    data=file.read(),
                    file_name=filename,
                    mime="application/pdf"
                )

        else:

            st.error("Customer Not Found")