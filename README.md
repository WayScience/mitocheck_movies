# mitocheck_movies
All information regarding the download and processing of Mitocheck whole movies from IDR study with accession idr0013 (screenA). Movies are downloaded with Aspera. 

## Aspera Downloader:

### Step 1: Install Aspera

Install Aspera high-speed transfer client as described at https://github.com/IBM/aspera-cli#installation. We used the direct installation method. On Ubuntu, the direct installation method is as follows:

1. Install Ruby on Ubuntu: `sudo apt install ruby-full`
2. Confirm Ruby install: `ruby --version`
3. Install aspera-cli gem: `gem install aspera-cli`
4. Upgrade aspera-cli gem to latest version: `gem update aspera-cli`
5. Install acsp: `ascli conf ascp install`
6. Confirm install and locate acsp (for step 1a): `ascli config ascp show`

### Step 1a: Allow Aspera to run without password

It is necessary to allow Aspera command line interface (ascp) to run without a password to use it more easily with python. In order to run ascp without a password do the following:


1. Type `sudo visudo` at the terminal to open the sudo permissions (sudoers) file
2. Find the line with: `%sudo   ALL=(ALL:ALL) ALL`
3. Below that line, insert the following line: `username  ALL=(ALL) NOPASSWD: path_to_aspera`
Note: `username` is your username and `path_to_aspera` can be found with `ascli config ascp show`
4. Save and exit the editor

### Step 2: Download Aspera Public Key
Download and Aspera public key. You will need the location of this key to use Aspera