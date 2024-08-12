db-start:
	brew services start mongodb-community

db-stop:
	brew services stop mongodb-community

server-start:
	cd server && python main.py