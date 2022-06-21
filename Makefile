# ----- linux -----
install-linux:
	@echo "Installing..."
	sudo cp dist/main /usr/local/bin/cryptomizer
	@echo "Done"

uninstall-linux:
	@echo "Uninstalling..."
	sudo rm /usr/local/bin/cryptomizer
	@echo "Done."

ctk := $(shell python -c 'import customtkinter;import os.path; print(os.path.split(customtkinter.__file__)[0]);')
build-linux:
	pyinstaller --noconfirm --onefile --windowed --name cryptomizer --icon assets/icon.ico --add-data "$(ctk):customtkinter/" src/main.py

clean-linux:
	rm -rf build cryptomizer.spec

# ----- windows -----
build-windows:
	pyinstaller --noconfirm --onefile --windowed --name cryptomizer --icon assets/icon.ico --add-data "$(ctk);customtkinter/" src/main.py

# ----- mac-os -----
build-macos: build-linux
