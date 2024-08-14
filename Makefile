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

check-os:
	@echo $(OS)

db-start:
	brew services start mongodb-community

db-stop:
	brew services stop mongodb-community

server-start:
	cd server && python main.py