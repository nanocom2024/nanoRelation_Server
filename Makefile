# set system envrion for Windows
ifeq ($(OS),Windows_NT)
    OS_NAME := windows
else
    UNAME_OS := $(shell uname -s)
    ifeq ($(UNAME_OS),Linux)
        OS_NAME := linux
    else ifeq ($(UNAME_OS),Darwin)
        OS_NAME := mac
    else
        OS_NAME:=unknown
    endif
endif


db-start:
	if [ $(OS_NAME) = "mac" ]; then \
		brew services start mongodb-community; \
	elif [ $(OS_NAME) = "linux" ]; then \
		sudo systemctl start mongod; \
	fi

db-stop:
	if [ $(OS_NAME) = "mac" ]; then \
		brew services stop mongodb-community; \
	elif [ $(OS_NAME) = "linux" ]; then \
		sudo systemctl stop mongod; \
	fi

server-start:
	cd server && python main.py