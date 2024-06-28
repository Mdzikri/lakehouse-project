docker run --name mysql-db -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=dataset_db -p 3306:3306 -d mysql:latest

pip install pymysql (python -c "import pymysql; print(pymysql.__version__))

