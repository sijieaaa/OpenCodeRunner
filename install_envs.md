


# CMake for C/C++
We use `cmake` for `C/C++` running. (https://cmake.org/download/)
```bash
wget https://github.com/Kitware/CMake/releases/download/v4.0.1/cmake-4.0.1-linux-x86_64.tar.gz
tar -xzvf cmake-4.0.1-linux-x86_64.tar.gz

# Add the following line into `~/.bashrc`
export PATH="ABSPATH_OF_{cmake-4.0.1-linux-x86_64/bin}:$PATH"
```



# Dafny
```bash
wget https://github.com/dafny-lang/dafny/releases/download/v4.10.0/dafny-4.10.0-x64-ubuntu-20.04.zip
unzip dafny-4.10.0-x64-ubuntu-20.04.zip

# Add the following line into `~/.bashrc`
export PATH="ABSPATH_OF_{dafny}:$PATH"
```
If you need `dotnet`:
```bash
sudo add-apt-repository ppa:dotnet/backports
sudo apt-get update && \
  sudo apt-get install -y dotnet-sdk-9.0
```



# Java
```bash
wget https://download.java.net/java/GA/jdk21/fd2272bbf8e04c3dbaee13770090416c/35/GPL/openjdk-21_linux-x64_bin.tar.gz
tar -xf openjdk-21_linux-x64_bin.tar.gz

# Add the following line into `~/.bashrc`
export JAVA_HOME="ABSPATH_of_{jdk-21}"
export PATH="$JAVA_HOME/bin:$PATH"
```


# JavaScript
We use `node.js` to run JS code (https://nodejs.org/en)
```bash
wget https://nodejs.org/dist/v22.14.0/node-v22.14.0-linux-x64.tar.xz
tar -xf node-v22.14.0-linux-x64.tar.xz

# Add the following line into `~/.bashrc`
export PATH="ABSPATH_of_{node-v22.14.0-linux-x64/bin}:$PATH"
```


# SQL (PostgreSQL)
We use `postgresql` for SQL running (https://www.postgresql.org/download/linux/ubuntu/).
```
sudo apt install postgresql
```



# Python
You can follow https://www.anaconda.com/docs/getting-started/miniconda/install#linux-terminal-installer for `miniconda` installation

Or `anaconda` in https://www.anaconda.com/docs/getting-started/anaconda/install#linux-installer


# TypeScript
We use `ts-node` to run TS code. This is installed using `npm` from `node.js`
```bash
npm install -g ts-node typescript
```