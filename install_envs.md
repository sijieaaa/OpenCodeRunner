

# Dafny
```bash
wget https://github.com/dafny-lang/dafny/releases/download/v4.10.0/dafny-4.10.0-x64-ubuntu-20.04.zip
unzip dafny-4.10.0-x64-ubuntu-20.04.zip
```
Modify `~/.bashrc` to include following lines:
```bash
export PATH="PATH_OF_dafny:$PATH"
```
```bash
sudo add-apt-repository ppa:dotnet/backports
sudo apt-get update && \
  sudo apt-get install -y dotnet-sdk-9.0
```



# Java
```bash
wget https://download.java.net/java/GA/jdk21/fd2272bbf8e04c3dbaee13770090416c/35/GPL/openjdk-21_linux-x64_bin.tar.gz
tar -xf openjdk-21_linux-x64_bin.tar.gz
```
Modify `~/.bashrc` to include following lines:
```bash
export JAVA_HOME="PATH_of_{jdk-21}"
export PATH="$JAVA_HOME/bin:$PATH"
```


# JavaScript
We use `node.js` to run JS code (https://nodejs.org/en)
```
wget https://nodejs.org/dist/v22.14.0/node-v22.14.0-linux-x64.tar.xz
tar -xf node-v22.14.0-linux-x64.tar.xz
```
Modify `~/.bashrc` to include following lines:
```bash
export PATH="PATH_of_{node-v22.14.0-linux-x64/bin}:$PATH"
```




# Python
You can follow https://www.anaconda.com/docs/getting-started/miniconda/install#linux-terminal-installer for miniconda installation


# TypeScript
We use `ts-node` to run TS code. This is installed using `npm` from `node.js`
```bash
npm install -g ts-node typescript
```