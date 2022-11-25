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
	mkdir dist
	python -m nuitka src/main.py --output-dir=dist --onefile --linux-onefile-icon=assets/icon.png --assume-yes-for-downloads --include-data-dir="$(ctk)=customtkinter/" --enable-plugin=tk-inter -o dist/cryptomizer.AppImage

# ----- windows -----
build-windows:
	mkdir dist
	python -m nuitka src/main.py --output-dir=dist --onefile --mingw64 --assume-yes-for-downloads --windows-disable-console --windows-icon-from-ico=assets/icon.ico --include-data-dir="$(ctk)=customtkinter/" --enable-plugin=tk-inter -o dist/cryptomizer.exe

# ----- mac-os -----
build-macos:
	mkdir dist
	python -m nuitka src/main.py --output-dir=dist --onefile --linux-onefile-icon=assets/icon.png --assume-yes-for-downloads --macos-disable-console --include-data-dir="$(ctk)=customtkinter/" -o dist/cryptomizer
