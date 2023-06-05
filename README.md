# SQL-Injection

SQL injection attacks are a type of attack where a malicious user is able to execute arbitrary SQL code on a database. This is usually done via a web application in order to gain access to sensitive data. An SQL injection attack is performed by exploiting vulnerabilities in the application's code, or by tricking users into submitting malicious input. This occurs when a code uses unsanitized data from user input in SQL statements, a malicious user includes SQL elements in the input stealthily, and when the code executes these SQL elements as part of legitimate SQL statements. This can be used to bypass authentication checks, retrieve sensitive data from a database, modify data, delete data, subvert application logic, conduct UNION attacks or even drop the database. Once the attacker has gained access to the database, they can view, modify, or delete data at will. This can lead to serious security implications, such as data leakage, loss and corruption, or identity theft. It may even lead to complete system compromise.

Our proposed system consists of **three phases**: 
1. Understanding SQL injection attacks by creating a database and exploiting the vulnerabilities
2. Detecting SQL injection attacks by finding vulnerabilities in queries and extracting forms from a website
3. Creating a GUI-based tool to detect and analyze these vulnerabilities on any given URL.

Our implemented system can conclusively state whether a given URL is SQL injection vulnerable or not. It can be used to test queries being submitted to the database, before actually returning the results obtained to the user. This can reduce loss of confidentiality of data or integrity of the database and can help drastically reduce the possibilities and likelihood of a SQL injection attack. Any queries submitted to the tool will be formatted with double quotes and tested through the Boolean function in the code to detect whether the passed query would result in an error in its response. In case an error statement is generated, the user would be redirected to a page on protection against SQL injection.

In case a malicious attacker submits a query that can cause damage to the data, users’ confidentiality, or the database itself, the attack can be detected immediately if it is made to pass through the tool created. We have tested our tool against both, safe queries as well as SQL injection queries on different URLs, and have found our results to be accurate. We have also been able to detect the number of forms on web pages and test the queries on these form input fields and actions.
