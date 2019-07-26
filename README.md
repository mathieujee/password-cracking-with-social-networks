

# Cracking Passwords With Social Networks

The goal of this project is to crack a user's password using his public personal data found on social networks. The hashed password of the target is needed. Hashcat will then try to crack this hash.

For now, the only social network supported is Facebook.



## Basic Requirements

- Make sure you have at least **Python 3.7** installed:

  ```bash
  python3 --version
  ```

  If not, please install one of the latest versions of Python3.



## Additional Requirements

- Facebook ID of the target (found in URL of the target's profile page)
- Hash of the password to be cracked



## OS Requirements

- Unix distrib (This project was only tested on Ubuntu 18 and Kali Linux)



## Install git 

```bash
sudo apt install git
```



## Install curl

```bash
sudo apt install curl
```



## Clone project

```bash
git clone https://github.com/mathieujee/password-cracking-with-social-networks.git
```



## Download rockyou.txt

```bash
curl -L https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -o extended_wordlists/rockyou.txt
```



## Install p7zip

```bash
sudo apt install p7zip
```



## Install Hashcat

- Download the latest version of hashcat:

  ```bash
  wget -P ~/Downloads/ https://hashcat.net/files/hashcat-5.0.0.7z
  ```

- Access the download directory:

  ```bash
  cd ~/Downloads/
  ```

- Unzip the file:

  ```bash
  sudo p7zip -d hashcat-5.0.0.7z
  ```

- Access the new unzipped folder:

  ```
  cd hashcat-5.0.0
  ```

- Run:

  ```bash
  sudo cp hashcat64.bin /usr/bin/
  ```

  ```bash
  sudo ln -s /usr/bin/hashcat64.bin /usr/bin/hashcat
  ```

  ```bash
  sudo cp -Rv OpenCL/ /usr/bin/
  ```

  ```bash
  sudo cp hashcat.hcstat2 /usr/bin/
  ```

  ```bash
  sudo cp hashcat.hctune /usr/bin/
  ```

- Test the installation with this command:

  ```bash
  sudo hashcat --benchmark
  ```

  

## Install pip3

``` bash
sudo apt install python3-pip
```



## Install pipenv

- ```
  pip3 install --user pipenv
  ```

- Edit `~/.profile` and add the following line at the end of the file:

  ```
  export PATH="$HOME/.local/bin:$PATH"
  ```

- Changes will take effect after running this command:

  ```bash
  source ~/.profile
  ```

- Specify Python3 for pipenv:

  ```bash
  pipenv --python path/to/python
  ```

  

## Install dependencies

- Go back inside the project root folder.

- Run:

  ```
  pipenv install
  ```

- If for some reasons, `pipenv install` doesn't work, you can still install each dependency one by one using `pip3`:

  ```
  pip3 install --user DEPENDENCY_NAME
  ```

  You can find all the dependencies in `./Pipfile`.

  

## Add hash file

- Create a file in the root folder of this project:

  ```bash
  touch hash.txt
  ```

- Add some hashes.

- Example of `hash.txt` containing 3 MD5 hashes:

  ```
  5f4dcc3b5aa765d61d8327deb882cf99
  25d55ad283aa400af464c76d713c07ad
  84d961568a65073a3bcf0eb216b2a576
  ```

  By default, the program supports MD5 hashes. You can modify the type of hash in `./utils/setup.py`:

  ```python
  # HASHCAT SETUP
  HASH_TYPE = '0'
  ```

  You can find a list of all hash types supported by hashcat with their value: 

  - https://hashcat.net/wiki/doku.php?id=example_hashes

## Setup your fake Facebook account

- Add the email and passowrd of your fake Facebook account in `./utils/setup.py`:
  ```python
  # Email used to login on the Facebook account
  EMAIL = 'YOUR@EMAIL.ADDRESS'

  # Password used to login on the Facebook account
  PASSWORD = 'YOUR_PASSWORD'
  ```
  
## Launch the attack

```bash
sudo python3 entry_point.py USER_ID
```

You can use this ID for tests purposes: `100039761583594`



## Results

- Cracked passwords (if there are) are shown in `./cracked.txt` file.
