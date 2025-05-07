import matplotlib.pyplot as plt
import mysql.connector

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="new_schema"
)

# Execute SQL query for orders count by region
cursor = db_connection.cursor()
sql_query_orders_count = """
    SELECT 
        `RegionDescription`,
        COUNT(DISTINCT `dbo.Orders`.`OrderID`) AS `orders_count`
    FROM 
        `dbo.Region`
    JOIN 
        `dbo.Territories` ON `dbo.Territories`.`RegionID` = `dbo.Region`.`RegionID`
    JOIN 
        `dbo.EmployeeTerritories` ON `dbo.Territories`.`TerritoryID` = `dbo.EmployeeTerritories`.`TerritoryID`
    JOIN 
        `dbo.Employees` ON `dbo.Employees`.`EmployeeID` = `dbo.EmployeeTerritories`.`EmployeeID`
    JOIN 
        `dbo.Orders` ON `dbo.Employees`.`EmployeeID` = `dbo.Orders`.`EmployeeID`
    GROUP BY 
        `dbo.Region`.`RegionDescription`
    ORDER BY 
        `orders_count` DESC;
"""
cursor.execute(sql_query_orders_count)
results_orders_count = cursor.fetchall()

# Execute SQL query for orders freight by region
sql_query_orders_freight = """
    SELECT 
        `RegionDescription`,
        SUM(`dbo.Orders`.`Freight`) AS `total_freight`
    FROM 
        `dbo.Region`
    JOIN 
        `dbo.Territories` ON `dbo.Territories`.`RegionID` = `dbo.Region`.`RegionID`
    JOIN 
        `dbo.EmployeeTerritories` ON `dbo.Territories`.`TerritoryID` = `dbo.EmployeeTerritories`.`TerritoryID`
    JOIN 
        `dbo.Employees` ON `dbo.Employees`.`EmployeeID` = `dbo.EmployeeTerritories`.`EmployeeID`
    JOIN 
        `dbo.Orders` ON `dbo.Employees`.`EmployeeID` = `dbo.Orders`.`EmployeeID`
    GROUP BY 
        `dbo.Region`.`RegionDescription`
    ORDER BY 
        `total_freight` DESC;
"""
cursor.execute(sql_query_orders_freight)
results_orders_freight = cursor.fetchall()

# Close database connection
cursor.close()
db_connection.close()

# Extract data for plotting orders count by region
region_descriptions_orders_count = [result[0] for result in results_orders_count]
orders_count = [result[1] for result in results_orders_count]

# Extract data for plotting orders freight by region
region_descriptions_orders_freight = [result[0] for result in results_orders_freight]
total_freight = [result[1] for result in results_orders_freight]

# Create pie chart for orders count by region
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.pie(orders_count, labels=region_descriptions_orders_count, autopct='%1.1f%%', startangle=140)
plt.title('Orders Count by Region')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

# Create pie chart for orders freight by region
plt.subplot(1, 2, 2)
plt.pie(total_freight, labels=region_descriptions_orders_freight, autopct='%1.1f%%', startangle=140)
plt.title('Total Freight by Region')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

# Adjust layout and display charts
plt.tight_layout()
plt.show()
