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
    SELECT 
        `dbo.Customers`.`CustomerID`,
        COUNT(DISTINCT `dbo.Orders`.`OrderID`) AS `OrdersCount`
    FROM 
        `dbo.Customers`
    JOIN 
        `dbo.Orders` ON `dbo.Customers`.`CustomerID` = `dbo.Orders`.`CustomerID`
    JOIN 
        `dbo.Order Details` ON `dbo.Orders`.`OrderID` = `dbo.Order Details`.`OrderID`
    GROUP BY 
        `dbo.Customers`.`CustomerID`
    ORDER BY 
        `OrdersCount` DESC
    LIMIT 10;
"""
cursor.execute(sql_query)
results = cursor.fetchall()

# Close database connection
cursor.close()
db_connection.close()

# Extract data for plotting
customer_ids = [result[0] for result in results]
order_counts = [result[1] for result in results]

# Create bar chart for top 10 customers by order count
plt.figure(figsize=(10, 6))
plt.bar(customer_ids, order_counts, color='skyblue')
plt.xlabel('Customer IDs')
plt.ylabel('Order Count')
plt.title('Top 10 Customers by Order Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Display the chart
plt.show()
