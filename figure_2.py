import matplotlib.pyplot as plt
import mysql.connector

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="new_schema"
)

# Execute SQL query
cursor = db_connection.cursor()
sql_query = """
    SELECT `dbo.Suppliers`.`CompanyName`, COUNT(`dbo.Order Details`.`Quantity`) AS `Quantity`
    FROM `dbo.Suppliers`
    JOIN `dbo.Products` ON `dbo.Products`.`SupplierID` = `dbo.Suppliers`.`SupplierID`
    JOIN `dbo.Order Details` ON `dbo.Products`.`ProductID` = `dbo.Order Details`.`ProductID`
    GROUP BY `dbo.Suppliers`.`CompanyName`
    ORDER BY `Quantity` DESC
    LIMIT 10;
"""
cursor.execute(sql_query)

# Fetch data
results = cursor.fetchall()

# Close database connection
cursor.close()
db_connection.close()

# Extract data for plotting
supplier_names = [result[0] for result in results]
order_quantities = [result[1] for result in results]

# Create bar chart
plt.figure(figsize=(10, 6))
plt.bar(supplier_names, order_quantities, color='skyblue')
plt.xlabel('Suppliers')
plt.ylabel('Order Quantity')
plt.title('Top 10 Suppliers by Order Quantity')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Display the chart
plt.show()
