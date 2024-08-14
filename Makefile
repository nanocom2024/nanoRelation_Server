# set system envrion for Windows
ifeq ($(OS),Windows_NT)
    GOOS := windows
else
    UNAME_OS := $(shell uname -s)
    ifeq ($(UNAME_OS),Linux)
        OS := linux
    else ifeq ($(UNAME_OS),Darwin)
        OS := mac
    else
        OS:=unknown
    endif
endif


db-start:
	if [ $(OS) = "mac" ]; then \
		brew services start mongodb-community; \
	elif [ $(OS) = "linux" ]; then \
		sudo systemctl start mongod; \
	fi

db-stop:
	if [ $(OS) = "mac" ]; then \
		brew services stop mongodb-community; \
	elif [ $(OS) = "linux" ]; then \
		sudo systemctl stop mongod; \
	fi

server-start:
	cd server && python main.py