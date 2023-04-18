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
	mkdir -p dist
	python -m nuitka src/main.py --output-dir=dist --onefile --linux-onefile-icon=assets/icon.png --assume-yes-for-downloads --include-data-dir="$(ctk)=customtkinter/" --enable-plugin=tk-inter -o cryptomizer.AppImage

# ----- windows -----
build-windows:
	mkdir -p dist
	python -m nuitka src/main.py --output-dir=dist --onefile --mingw64 --assume-yes-for-downloads --windows-disable-console --windows-icon-from-ico=assets/icon.ico --include-data-dir="$(ctk)=customtkinter/" --enable-plugin=tk-inter -o cryptomizer.exe

# ----- mac-os -----
build-macos:
	mkdir -p dist
	python -m nuitka src/main.py --output-dir=dist --onefile --linux-onefile-icon=assets/icon.png --assume-yes-for-downloads --macos-disable-console --macos-create-app-bundle --include-data-dir="$(ctk)=customtkinter/" -o cryptomizer
