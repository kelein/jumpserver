# Install cryptography error: build/temp.macosx-10.13-intel-2.7/_openssl.c:483:10: fatal error: 'openssl/opensslv.h' file not found

$ pip install cryptography --global-option=build_ext --global-option="-L/opt/homebrew/Cellar/openssl@3/3.1.1_1/lib" --global-option="-I/opt/homebrew/Cellar/openssl@3/3.1.1_1/include"


# Pillow zlib failed
# Reinstall xcode reslove

$ xcode-select --install


# libxmlsec 报错
wget 'https://raw.githubusercontent.com/Homebrew/homebrew-core/7f35e6ede954326a10949891af2dba47bbe1fc17/Formula/libxmlsec1.rb'
brew install ./libxmlsec1.rb

# libxmlsec1
