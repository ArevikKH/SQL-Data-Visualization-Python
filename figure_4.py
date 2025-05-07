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
        `dbo.Employees`.`FirstName`,
        COUNT(DISTINCT `dbo.Orders`.`OrderID`) AS `OrdersCount`
    FROM 
        `dbo.Employees`
    JOIN 
        `dbo.Orders` ON `dbo.Employees`.`EmployeeID` = `dbo.Orders`.`EmployeeID`
    JOIN 
        `dbo.Order Details` ON `dbo.Orders`.`OrderID` = `dbo.Order Details`.`OrderID`
    GROUP BY 
        `dbo.Employees`.`FirstName`
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
employee_names = [result[0] for result in results]
order_counts = [result[1] for result in results]

# Create bar chart for top 10 employees by order count
plt.figure(figsize=(10, 6))
plt.bar(employee_names, order_counts, color='#9370DB')  # Changed color to light purple
plt.xlabel('Employee Names')
plt.ylabel('Order Count')
plt.title('Top 10 Employees by Order Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Display the chart
plt.show()