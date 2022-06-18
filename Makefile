all: build clean

ctk := $(shell pip show customtkinter | grep "Location" | awk '{ print $$2 }')

build:
	pyinstaller --noconfirm --onefile --windowed --add-data "$(ctk)/customtkinter:customtkinter/" src/main.py

clean:
	rm -rf build main.spec

install:
	@echo "Installing..."
	sudo cp dist/main /usr/local/bin/cryptomizer
	@echo "Done"

uninstall:
	@echo "Uninstalling..."
	sudo rm /usr/local/bin/cryptomizer
	@echo "Done."