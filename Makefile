# ----- linux -----
install-linux:
	@echo "Installing..."
	sudo cp dist/main /usr/local/bin/cryptomizer
	@echo "Done"

uninstall-linux:
	@echo "Uninstalling..."
	sudo rm /usr/local/bin/cryptomizer
	@echo "Done."

ctk-linux := $(shell pip show customtkinter | grep "Location" | awk '{ print $$2 }')
build-linux:
	pyinstaller --noconfirm --onefile --windowed --add-data "$(ctk-linux)/customtkinter:customtkinter/" src/main.py

clean-linux:
	rm -rf build main.spec

# ----- windows -----
build-windows:
	pyinstaller --noconfirm --onefile --windowed --add-data "$(ctk-linux)/customtkinter;customtkinter/" src/main.py

# ----- mac-os -----
#build-mac:
#...
