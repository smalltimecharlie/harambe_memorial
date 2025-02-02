# Database Setup and Management

## **Setting Up the Database**
This script initializes the SQLite database, creates all necessary tables, and populates them with example data.

### **1️⃣ Running the Setup Script**
To create and populate the database with sample data, run the following command:

```sh
python setup_db_script.py
```

This will create a SQLite database file (`golf_society.db`) in the project directory.

---

## **Tearing Down the Database**
If you want to delete all tables and reset the database, run:

```sh
python setup_db_script.py --drop
```

This will remove all tables from the database.

---

## **Database Schema Overview**
The following tables will be created:

- **users**: Stores player information (name, handicap, role)
- **courses**: Stores golf course details (name, location, par, slope rating, course rating)
- **competitions**: Stores competition details (name, type, start date, end date)
- **rounds**: Tracks rounds played (player, competition, course, score, date played)
- **scores**: Stores detailed hole-by-hole scores for rounds

---

## **Example Data Populated**
The script will automatically insert:
- **3 players**: `Tiger Woods`, `Rory McIlroy`, and `Jon Rahm`
- **2 courses**: `Augusta National` and `St. Andrews`
- **2 competitions**: `Masters Tournament` and `The Open Championship`
- **6 rounds**: Each player competes in both competitions
- **Hole-by-hole scores for one round**

---

## **Troubleshooting**
- If the script fails, ensure you have Python 3 installed.
- If you need to manually delete the database file, run:

```sh
rm golf_society.db
```

Then re-run the setup script.
